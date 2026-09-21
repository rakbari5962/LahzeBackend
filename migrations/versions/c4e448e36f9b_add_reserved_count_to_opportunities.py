"""add reserved_count to opportunities

Revision ID: c4e448e36f9b
Revises: 2485361c456e
Create Date: 2026-09-21 22:22:29.962049

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c4e448e36f9b'

down_revision: Union[str, Sequence[str], None] = '2485361c456e'

branch_labels = None

depends_on = None



def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'opportunities',
        sa.Column(
            'reserved_count',
            sa.Integer(),
            nullable=False,
            server_default='0'
        )
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        'opportunities',
        'reserved_count'
    )