"""add temporary flag to sessions

Revision ID: 6c6980ddc925
Revises: 6b7460ca63a1
Create Date: 2026-09-12 17:15:19.742988

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c6980ddc925"
down_revision: Union[str, Sequence[str], None] = "4ab2815a2cd8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "sessions",
        sa.Column(
            "is_temporary",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "sessions",
        "is_temporary"
    )