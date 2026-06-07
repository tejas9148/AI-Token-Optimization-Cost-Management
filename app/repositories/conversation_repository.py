from decimal import Decimal

from sqlalchemy import Integer, func
from sqlalchemy.orm import Session

from app.models.conversation import Conversation, ConversationMessage


def get_conversation(db: Session, conversation_id: str) -> Conversation | None:
    """Return a conversation by its public identifier."""

    return db.get(Conversation, conversation_id)


def create_conversation(db: Session, *, conversation_id: str) -> Conversation:
    """Create and persist a new conversation row."""

    conversation = Conversation(conversation_id=conversation_id)
    db.add(conversation)
    db.flush()
    return conversation


def list_conversations(db: Session, *, offset: int, limit: int) -> list[Conversation]:
    """Return conversations ordered by most recently updated."""

    return (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc(), Conversation.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def count_conversations(db: Session) -> int:
    """Return the total number of conversations."""

    return db.query(Conversation).count()


def list_conversation_messages(db: Session, *, conversation_id: str) -> list[ConversationMessage]:
    """Return all persisted messages for a conversation."""

    return (
        db.query(ConversationMessage)
        .filter(ConversationMessage.conversation_id == conversation_id)
        .order_by(ConversationMessage.created_at.asc(), ConversationMessage.id.asc())
        .all()
    )


def create_conversation_message(
    db: Session,
    *,
    conversation_id: str,
    user_message: str,
    assistant_message: str,
    original_context_tokens: int,
    compressed_context_tokens: int,
    context_tokens_saved: int,
    compression_percentage: Decimal,
    summary_generated: bool,
    used_summary: bool,
) -> ConversationMessage:
    """Persist a conversation turn and return the stored row."""

    message = ConversationMessage(
        conversation_id=conversation_id,
        user_message=user_message,
        assistant_message=assistant_message,
        original_context_tokens=original_context_tokens,
        compressed_context_tokens=compressed_context_tokens,
        context_tokens_saved=context_tokens_saved,
        compression_percentage=compression_percentage,
        summary_generated=summary_generated,
        used_summary=used_summary,
    )
    db.add(message)
    db.flush()
    return message


def update_conversation_summary(
    db: Session,
    *,
    conversation: Conversation,
    summary_text: str,
    summary_tokens: int,
    context_tokens_saved: int,
    compression_percentage: Decimal,
) -> Conversation:
    """Store the latest summary and cumulative compression metrics for a conversation."""

    previous_summary_count = conversation.total_summaries_generated
    conversation.summary_text = summary_text
    conversation.summary_tokens = summary_tokens
    conversation.total_context_tokens_saved += context_tokens_saved
    conversation.total_summaries_generated = previous_summary_count + 1

    if previous_summary_count:
        weighted_total = (conversation.average_compression_percentage * Decimal(previous_summary_count)) + compression_percentage
        conversation.average_compression_percentage = weighted_total / Decimal(previous_summary_count + 1)
    else:
        conversation.average_compression_percentage = compression_percentage

    db.flush()
    return conversation


def get_conversation_analytics(db: Session) -> dict[str, int | Decimal | float]:
    """Return aggregated conversation compression metrics."""

    total_context_tokens_saved, total_summaries_generated, average_compression_percentage = (
        db.query(
            func.coalesce(func.sum(ConversationMessage.context_tokens_saved), 0),
            func.coalesce(func.sum(func.cast(ConversationMessage.summary_generated, Integer)), 0),
            func.coalesce(func.avg(ConversationMessage.compression_percentage), 0),
        ).one()
    )

    return {
        "total_context_tokens_saved": int(total_context_tokens_saved),
        "total_summaries_generated": int(total_summaries_generated),
        "average_compression_percentage": float(average_compression_percentage),
    }