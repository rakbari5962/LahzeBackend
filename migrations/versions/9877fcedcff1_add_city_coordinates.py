
"""add city coordinates

Revision ID: 9877fcedcff1
Revises: b11dfc61019f
Create Date: 2026-10-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9877fcedcff1"
down_revision: Union[str, Sequence[str], None] = "b11dfc61019f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "cities",
        sa.Column("latitude", sa.Float(), nullable=True),
    )
    op.add_column(
        "cities",
        sa.Column("longitude", sa.Float(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("cities", "longitude")
    op.drop_column("cities", "latitude")
