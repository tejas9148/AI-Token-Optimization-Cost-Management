"""create conversations tables

Revision ID: 20260607_0004
Revises: 20260606_0003
Create Date: 2026-06-07 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260607_0004"
down_revision = "20260606_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "conversations",
        sa.Column("conversation_id", sa.String(length=36), nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=True),
        sa.Column("summary_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_context_tokens_saved", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_summaries_generated", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("average_compression_percentage", sa.Numeric(6, 2), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("conversation_id"),
    )

    op.create_table(
        "conversation_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.String(length=36), nullable=False),
        sa.Column("user_message", sa.Text(), nullable=False),
        sa.Column("assistant_message", sa.Text(), nullable=False),
        sa.Column("original_context_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("compressed_context_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("context_tokens_saved", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("compression_percentage", sa.Numeric(6, 2), nullable=False, server_default="0"),
        sa.Column("summary_generated", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("used_summary", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.conversation_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_conversation_messages_conversation_id"),
        "conversation_messages",
        ["conversation_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_conversation_messages_conversation_id"), table_name="conversation_messages")
    op.drop_table("conversation_messages")
    op.drop_table("conversations")