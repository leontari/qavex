"""
Create users table.

Revision ID: 20240511_01
Revises:
Create Date: 2024-05-11
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = "20240511_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply the migration."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "email", sa.String(), nullable=False, unique=True, index=True
        ),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )


def downgrade() -> None:
    """Revert the migration."""
    op.drop_table("users")
