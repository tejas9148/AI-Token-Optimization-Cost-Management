"""add served_from_cache to ai_requests

Revision ID: 20260605_0002
Revises: 20260604_0001
Create Date: 2026-06-05 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260605_0002"
down_revision = "20260604_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "ai_requests",
        sa.Column("served_from_cache", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.alter_column("ai_requests", "served_from_cache", server_default=None)


def downgrade() -> None:
    op.drop_column("ai_requests", "served_from_cache")