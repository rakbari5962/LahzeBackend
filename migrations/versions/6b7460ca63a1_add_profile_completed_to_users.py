"""add profile completed to users

Revision ID: 6b7460ca63a1
Revises: d20e54b1d2f5
Create Date: 2026-09-12 14:41:47.132703

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6b7460ca63a1"
down_revision: Union[str, Sequence[str], None] = "d20e54b1d2f5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "profile_completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "users",
        "profile_completed"
    )