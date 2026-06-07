from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.config.settings import Settings
from app.models.conversation import Conversation, ConversationMessage
from app.repositories.conversation_repository import (
    count_conversations,
    create_conversation,
    create_conversation_message,
    get_conversation,
    get_conversation_analytics,
    list_conversation_messages,
    list_conversations,
    update_conversation_summary,
)
from app.schemas.chat import (
    ChatResponse,
    ConversationDetailResponse,
    ConversationListResponse,
    ConversationMessageItem,
)
from app.services.gemini_service import GeminiService, GeminiServiceError
from app.services.summarization_service import SummarizationService
from app.utils.token_utils import calculate_total_tokens


@dataclass(slots=True)
class ConversationService:
    """Orchestrate conversation storage, context compression, and Gemini responses."""

    settings: Settings
    db: Session

    def chat(self, *, conversation_id: str | None, user_message: str) -> ChatResponse:
        """Handle a chat turn with fail-open summarization."""

        conversation = self._get_or_create_conversation(conversation_id)
        prior_messages = list_conversation_messages(self.db, conversation_id=conversation.conversation_id)

        original_context_text = self._build_context_text(
            summary_text=conversation.summary_text,
            messages=prior_messages,
            current_user_message=user_message,
        )
        original_context_tokens = self._count_tokens(original_context_text)

        summary_text = conversation.summary_text
        summary_generated = False
        used_summary = summary_text is not None

        compressed_messages: list[ConversationMessage] = prior_messages[-4:] if used_summary else prior_messages
        if original_context_tokens > self.settings.summary_trigger_tokens and prior_messages:
            summary_text, summary_generated = self._maybe_generate_summary(conversation, prior_messages)
            if summary_generated and summary_text:
                used_summary = True
                compressed_messages = prior_messages[-4:]
        elif used_summary:
            compressed_messages = prior_messages[-4:]

        compressed_context_text = self._build_context_text(
            summary_text=summary_text,
            messages=compressed_messages,
            current_user_message=user_message,
        )
        compressed_context_tokens = self._count_tokens(compressed_context_text)
        if not used_summary:
            compressed_context_tokens = original_context_tokens

        gemini_service = GeminiService(settings=self.settings)
        assistant_message = gemini_service.generate_response(compressed_context_text)
        response_tokens = self._count_tokens(assistant_message)
        _ = calculate_total_tokens(compressed_context_tokens, response_tokens)

        context_tokens_saved = max(original_context_tokens - compressed_context_tokens, 0)
        compression_percentage = self._calculate_percentage(original_context_tokens, compressed_context_tokens)

        if used_summary:
            update_conversation_summary(
                self.db,
                conversation=conversation,
                summary_text=summary_text or "",
                summary_tokens=self._count_tokens(summary_text) if summary_text else 0,
                context_tokens_saved=context_tokens_saved,
                compression_percentage=compression_percentage,
            )

        message = create_conversation_message(
            self.db,
            conversation_id=conversation.conversation_id,
            user_message=user_message,
            assistant_message=assistant_message,
            original_context_tokens=original_context_tokens,
            compressed_context_tokens=compressed_context_tokens,
            context_tokens_saved=context_tokens_saved,
            compression_percentage=compression_percentage,
            summary_generated=summary_generated,
            used_summary=used_summary,
        )

        self.db.commit()
        self.db.refresh(conversation)
        self.db.refresh(message)

        return ChatResponse(
            success=True,
            conversation_id=conversation.conversation_id,
            user_message=user_message,
            assistant_message=assistant_message,
            summary_text=summary_text if used_summary else conversation.summary_text,
            original_context_tokens=original_context_tokens,
            compressed_context_tokens=compressed_context_tokens,
            context_tokens_saved=context_tokens_saved,
            compression_percentage=compression_percentage,
            summary_generated=summary_generated,
            used_summary=used_summary,
            created_at=message.created_at,
        )

    def get_conversations(self, *, page: int, page_size: int) -> ConversationListResponse:
        """Return a paginated list of conversations."""

        offset = (page - 1) * page_size
        total_items = count_conversations(self.db)
        items = list_conversations(self.db, offset=offset, limit=page_size)
        total_pages = (total_items + page_size - 1) // page_size if total_items else 0

        return ConversationListResponse(
            items=items,
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
        )

    def get_conversation(self, conversation_id: str) -> ConversationDetailResponse | None:
        """Return a conversation with all stored messages."""

        conversation = get_conversation(self.db, conversation_id)
        if conversation is None:
            return None

        messages = list_conversation_messages(self.db, conversation_id=conversation_id)
        return ConversationDetailResponse(
            conversation_id=conversation.conversation_id,
            summary_text=conversation.summary_text,
            summary_tokens=conversation.summary_tokens,
            total_context_tokens_saved=conversation.total_context_tokens_saved,
            total_summaries_generated=conversation.total_summaries_generated,
            average_compression_percentage=conversation.average_compression_percentage,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[ConversationMessageItem.model_validate(message) for message in messages],
        )

    def get_analytics(self) -> dict[str, int | Decimal | float]:
        """Return conversation-specific compression metrics."""

        return get_conversation_analytics(self.db)

    def _get_or_create_conversation(self, conversation_id: str | None) -> Conversation:
        if conversation_id:
            conversation = get_conversation(self.db, conversation_id)
            if conversation is not None:
                return conversation

        new_conversation_id = conversation_id or str(uuid4())
        return create_conversation(self.db, conversation_id=new_conversation_id)

    def _build_context_text(
        self,
        *,
        summary_text: str | None,
        messages: list[ConversationMessage],
        current_user_message: str,
    ) -> str:
        parts: list[str] = []
        if summary_text:
            parts.append(f"Conversation summary:\n{summary_text.strip()}")

        if messages:
            transcript_lines: list[str] = ["Recent conversation:"]
            for message in messages:
                transcript_lines.append(f"User: {message.user_message.strip()}")
                transcript_lines.append(f"Assistant: {message.assistant_message.strip()}")
            parts.append("\n".join(transcript_lines))

        parts.append(f"Current user message:\n{current_user_message.strip()}")
        return "\n\n".join(parts).strip()

    def _maybe_generate_summary(
        self,
        conversation: Conversation,
        messages: list[ConversationMessage],
    ) -> tuple[str | None, bool]:
        summary_service = SummarizationService(settings=self.settings)
        messages_text = self._format_messages(messages)

        try:
            return summary_service.summarize(existing_summary=conversation.summary_text, messages_text=messages_text), True
        except GeminiServiceError:
            return conversation.summary_text, False
        except Exception:
            return conversation.summary_text, False

    def _format_messages(self, messages: list[ConversationMessage]) -> str:
        lines: list[str] = []
        for message in messages:
            lines.append(f"User: {message.user_message.strip()}")
            lines.append(f"Assistant: {message.assistant_message.strip()}")
        return "\n".join(lines)

    def _count_tokens(self, text: str) -> int:
        gemini_service = GeminiService(settings=self.settings)
        return gemini_service.count_tokens(text)

    def _calculate_percentage(self, original_tokens: int, compressed_tokens: int) -> Decimal:
        if original_tokens <= 0:
            return Decimal("0")

        saved_tokens = max(original_tokens - compressed_tokens, 0)
        return (Decimal(saved_tokens) / Decimal(original_tokens) * Decimal("100")).quantize(Decimal("0.01"))