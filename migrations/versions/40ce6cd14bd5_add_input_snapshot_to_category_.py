"""add input snapshot to category suggestions

Revision ID: 40ce6cd14bd5
Revises: a123dd789afb
Create Date: 2026-09-12 21:58:20.677031

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40ce6cd14bd5'
down_revision: Union[str, Sequence[str], None] = 'a123dd789afb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""


    op.add_column(
        'category_suggestions',
        sa.Column(
            'input_snapshot',
            sa.JSON(),
            nullable=True
        )
    )



def downgrade() -> None:
    """Downgrade schema."""


    op.drop_column(
        'category_suggestions',
        'input_snapshot'
    )