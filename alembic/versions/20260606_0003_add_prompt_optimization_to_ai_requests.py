"""add prompt optimization fields to ai_requests

Revision ID: 20260606_0003
Revises: 20260605_0002
Create Date: 2026-06-06 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260606_0003"
down_revision = "20260605_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("ai_requests", sa.Column("original_prompt", sa.Text(), nullable=True))
    op.add_column("ai_requests", sa.Column("optimized_prompt", sa.Text(), nullable=True))
    op.add_column("ai_requests", sa.Column("original_input_tokens", sa.Integer(), nullable=True))
    op.add_column("ai_requests", sa.Column("optimized_input_tokens", sa.Integer(), nullable=True))
    op.add_column("ai_requests", sa.Column("tokens_saved", sa.Integer(), nullable=True))
    op.add_column("ai_requests", sa.Column("savings_percentage", sa.Numeric(6, 2), nullable=True))

    op.execute("UPDATE ai_requests SET original_prompt = prompt WHERE original_prompt IS NULL")
    op.execute("UPDATE ai_requests SET optimized_prompt = prompt WHERE optimized_prompt IS NULL")
    op.execute("UPDATE ai_requests SET original_input_tokens = input_tokens WHERE original_input_tokens IS NULL")
    op.execute("UPDATE ai_requests SET optimized_input_tokens = input_tokens WHERE optimized_input_tokens IS NULL")
    op.execute("UPDATE ai_requests SET tokens_saved = 0 WHERE tokens_saved IS NULL")
    op.execute("UPDATE ai_requests SET savings_percentage = 0 WHERE savings_percentage IS NULL")

    op.alter_column("ai_requests", "original_prompt", nullable=False)
    op.alter_column("ai_requests", "optimized_prompt", nullable=False)
    op.alter_column("ai_requests", "original_input_tokens", nullable=False)
    op.alter_column("ai_requests", "optimized_input_tokens", nullable=False)
    op.alter_column("ai_requests", "tokens_saved", nullable=False)
    op.alter_column("ai_requests", "savings_percentage", nullable=False)


def downgrade() -> None:
    op.drop_column("ai_requests", "savings_percentage")
    op.drop_column("ai_requests", "tokens_saved")
    op.drop_column("ai_requests", "optimized_input_tokens")
    op.drop_column("ai_requests", "original_input_tokens")
    op.drop_column("ai_requests", "optimized_prompt")
    op.drop_column("ai_requests", "original_prompt")