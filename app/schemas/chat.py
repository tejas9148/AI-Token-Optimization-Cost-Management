from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChatRequest(BaseModel):
    """Request payload for the /chat endpoint."""

    conversation_id: str | None = Field(default=None, description="Optional conversation identifier")
    user_message: str = Field(..., description="Message sent by the user")

    @field_validator("user_message")
    @classmethod
    def validate_user_message(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("User message cannot be empty.")
        return normalized


class ChatResponse(BaseModel):
    """Response payload returned by the /chat endpoint."""

    success: bool
    conversation_id: str
    user_message: str
    assistant_message: str
    summary_text: str | None
    original_context_tokens: int
    compressed_context_tokens: int
    context_tokens_saved: int
    compression_percentage: Decimal
    summary_generated: bool
    used_summary: bool
    created_at: datetime


class ConversationListItem(BaseModel):
    """Summary view of a conversation for list endpoints."""

    model_config = ConfigDict(from_attributes=True)

    conversation_id: str
    summary_text: str | None
    summary_tokens: int
    total_context_tokens_saved: int
    total_summaries_generated: int
    average_compression_percentage: Decimal
    created_at: datetime
    updated_at: datetime


class ConversationMessageItem(BaseModel):
    """Single persisted turn in a conversation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_message: str
    assistant_message: str
    original_context_tokens: int
    compressed_context_tokens: int
    context_tokens_saved: int
    compression_percentage: Decimal
    summary_generated: bool
    used_summary: bool
    created_at: datetime


class ConversationDetailResponse(BaseModel):
    """Detailed conversation payload including all stored turns."""

    model_config = ConfigDict(from_attributes=True)

    conversation_id: str
    summary_text: str | None
    summary_tokens: int
    total_context_tokens_saved: int
    total_summaries_generated: int
    average_compression_percentage: Decimal
    created_at: datetime
    updated_at: datetime
    messages: list[ConversationMessageItem]


class ConversationListResponse(BaseModel):
    """Paginated list of conversations."""

    items: list[ConversationListItem]
    page: int
    page_size: int
    total_items: int
    total_pages: int