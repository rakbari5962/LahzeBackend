"""create business referral shares table

Revision ID: 15eaa8e78a16
Revises: 73b0af8b079c
Create Date: 2026-09-11 13:02:11.752108

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15eaa8e78a16'
down_revision: Union[str, Sequence[str], None] = '73b0af8b079c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'business_referral_shares',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'business_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'user_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'role',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'percentage',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'status',
            sa.String(),
            nullable=False,
            server_default='ACTIVE'
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id']
        ),

        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id']
        ),

        sa.PrimaryKeyConstraint(
            'id'
        )
    )


    op.create_index(
        'ix_business_referral_shares_id',
        'business_referral_shares',
        ['id'],
        unique=False
    )


    op.create_index(
        'ix_business_referral_shares_business_id',
        'business_referral_shares',
        ['business_id'],
        unique=False
    )


    op.create_index(
        'ix_business_referral_shares_user_id',
        'business_referral_shares',
        ['user_id'],
        unique=False
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table(
        'business_referral_shares'
    )