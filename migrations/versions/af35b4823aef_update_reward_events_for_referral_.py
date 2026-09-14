"""update reward events for referral rewards

Revision ID: af35b4823aef
Revises: 15eaa8e78a16
Create Date: 2026-09-11 13:29:58.137372

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af35b4823aef'
down_revision: Union[str, Sequence[str], None] = '15eaa8e78a16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""


    # اضافه کردن ارتباط Reward با Business
    op.add_column(
        'reward_events',
        sa.Column(
            'business_id',
            sa.Integer(),
            nullable=True
        )
    )


    # ارتباط با تراکنش مالی
    op.add_column(
        'reward_events',
        sa.Column(
            'transaction_id',
            sa.String(),
            nullable=True
        )
    )


    # Booking برای بعضی Rewardها اختیاری می‌شود
    op.alter_column(
        'reward_events',
        'booking_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )


    # Review برای Rewardهای جدید اختیاری می‌شود
    # ولی حذف نمی‌شود چون در آینده Review Reward داریم
    op.alter_column(
        'reward_events',
        'review_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )


    # Index برای Business
    op.create_index(
        'ix_reward_events_business_id',
        'reward_events',
        ['business_id'],
        unique=False
    )


    # Index برای Transaction
    op.create_index(
        'ix_reward_events_transaction_id',
        'reward_events',
        ['transaction_id'],
        unique=False
    )


    # Foreign Key Business
    op.create_foreign_key(
        'fk_reward_events_business',
        'reward_events',
        'businesses',
        ['business_id'],
        ['id']
    )



def downgrade() -> None:
    """Downgrade schema."""


    # حذف Foreign Key Business
    op.drop_constraint(
        'fk_reward_events_business',
        'reward_events',
        type_='foreignkey'
    )


    # حذف Indexها
    op.drop_index(
        'ix_reward_events_transaction_id',
        table_name='reward_events'
    )


    op.drop_index(
        'ix_reward_events_business_id',
        table_name='reward_events'
    )


    # برگرداندن حالت قبلی Review
    op.alter_column(
        'reward_events',
        'review_id',
        existing_type=sa.INTEGER(),
        nullable=False
    )


    # برگرداندن حالت قبلی Booking
    op.alter_column(
        'reward_events',
        'booking_id',
        existing_type=sa.INTEGER(),
        nullable=False
    )


    # حذف ستون‌های جدید
    op.drop_column(
        'reward_events',
        'transaction_id'
    )


    op.drop_column(
        'reward_events',
        'business_id'
    )