"""add business profile fields

Revision ID: 874e33157104
Revises: 40ce6cd14bd5
Create Date: 2026-09-13 19:57:36.054224

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "874e33157104"

down_revision: Union[str, Sequence[str], None] = "40ce6cd14bd5"

branch_labels = None

depends_on = None



def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "businesses",
        sa.Column(
            "description",
            sa.String(),
            nullable=True
        )
    )


    op.add_column(
        "businesses",
        sa.Column(
            "phone",
            sa.String(),
            nullable=True
        )
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "businesses",
        "phone"
    )


    op.drop_column(
        "businesses",
        "description"
    )