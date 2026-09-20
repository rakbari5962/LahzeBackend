"""add opportunity profile fields to users

Revision ID: 2485361c456e
Revises: 204246a91490
Create Date: 2026-09-20 22:30:42.287651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2485361c456e'
down_revision: Union[str, Sequence[str], None] = '204246a91490'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'users',
        sa.Column(
            'first_name',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'last_name',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'gender',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'birth_date',
            sa.Date(),
            nullable=True
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'iban',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'education',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'email',
            sa.String(),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        'users',
        'email'
    )

    op.drop_column(
        'users',
        'education'
    )

    op.drop_column(
        'users',
        'iban'
    )

    op.drop_column(
        'users',
        'birth_date'
    )

    op.drop_column(
        'users',
        'gender'
    )

    op.drop_column(
        'users',
        'last_name'
    )

    op.drop_column(
        'users',
        'first_name'
    )
