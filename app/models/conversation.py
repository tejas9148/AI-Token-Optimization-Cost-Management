from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Conversation(Base):
    """Persist a logical chat conversation and its latest summary state."""

    __tablename__ = "conversations"

    conversation_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_context_tokens_saved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_summaries_generated: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    average_compression_percentage: Mapped[Decimal] = mapped_column(
        Numeric(6, 2), nullable=False, default=Decimal("0")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    messages: Mapped[list["ConversationMessage"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ConversationMessage.created_at.asc()",
    )


class ConversationMessage(Base):
    """Persist a single conversation turn with compression metadata."""

    __tablename__ = "conversation_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversations.conversation_id", ondelete="CASCADE"), nullable=False
    )
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    assistant_message: Mapped[str] = mapped_column(Text, nullable=False)
    original_context_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    compressed_context_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    context_tokens_saved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    compression_percentage: Mapped[Decimal] = mapped_column(
        Numeric(6, 2), nullable=False, default=Decimal("0")
    )
    summary_generated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    used_summary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    conversation: Mapped[Conversation] = relationship(back_populates="messages")