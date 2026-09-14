"""add reward idempotency key

Revision ID: d20e54b1d2f5
Revises: af35b4823aef
Create Date: 2026-09-11 14:07:39.689560

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'd20e54b1d2f5'
down_revision: Union[str, Sequence[str], None] = 'af35b4823aef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""


    # مرحله اول:
    # اضافه کردن ستون به صورت nullable

    op.add_column(
        'reward_events',
        sa.Column(
            'idempotency_key',
            sa.String(),
            nullable=True
        )
    )


    op.create_index(
        'ix_reward_events_idempotency_key',
        'reward_events',
        ['idempotency_key'],
        unique=True
    )



def downgrade() -> None:
    """Downgrade schema."""


    op.drop_index(
        'ix_reward_events_idempotency_key',
        table_name='reward_events'
    )


    op.drop_column(
        'reward_events',
        'idempotency_key'
    )