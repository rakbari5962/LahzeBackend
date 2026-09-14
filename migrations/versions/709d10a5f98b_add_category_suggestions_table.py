"""add category suggestions table

Revision ID: 709d10a5f98b
Revises: 7063592c1967
Create Date: 2026-09-12 20:39:01.481664

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '709d10a5f98b'
down_revision: Union[str, Sequence[str], None] = '7063592c1967'
branch_labels = None
depends_on = None



def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'category_suggestions',

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
            'suggested_category_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'confidence',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'reason',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'status',
            sa.String(),
            nullable=False
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

        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id']
        ),

        sa.ForeignKeyConstraint(
            ['suggested_category_id'],
            ['business_categories.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )


    op.create_index(
        op.f('ix_category_suggestions_business_id'),
        'category_suggestions',
        ['business_id'],
        unique=False
    )


    op.create_index(
        op.f('ix_category_suggestions_id'),
        'category_suggestions',
        ['id'],
        unique=False
    )


    op.create_index(
        op.f('ix_category_suggestions_suggested_category_id'),
        'category_suggestions',
        ['suggested_category_id'],
        unique=False
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f('ix_category_suggestions_suggested_category_id'),
        table_name='category_suggestions'
    )


    op.drop_index(
        op.f('ix_category_suggestions_id'),
        table_name='category_suggestions'
    )


    op.drop_index(
        op.f('ix_category_suggestions_business_id'),
        table_name='category_suggestions'
    )


    op.drop_table(
        'category_suggestions'
    )