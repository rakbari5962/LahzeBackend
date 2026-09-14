"""add business categories table

Revision ID: 9c1abaa58bac
Revises: 6c6980ddc925
Create Date: 2026-09-12 20:25:27.968821

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c1abaa58bac'

down_revision: Union[str, Sequence[str], None] = '6c6980ddc925'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(

        'business_categories',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'slug',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'description',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),

        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            nullable=True
        ),

        sa.PrimaryKeyConstraint(
            'id'
        )
    )


    op.create_index(
        'ix_business_categories_id',
        'business_categories',
        ['id'],
        unique=False
    )


    op.create_index(
        'ix_business_categories_slug',
        'business_categories',
        ['slug'],
        unique=True
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        'ix_business_categories_slug',
        table_name='business_categories'
    )


    op.drop_index(
        'ix_business_categories_id',
        table_name='business_categories'
    )


    op.drop_table(
        'business_categories'
    )