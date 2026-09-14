"""add category ai history table

Revision ID: a123dd789afb
Revises: 709d10a5f98b
Create Date: 2026-09-12 21:51:34.691682

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a123dd789afb'
down_revision: Union[str, Sequence[str], None] = '709d10a5f98b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'category_ai_history',

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
            'suggestion_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'suggested_category_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'action',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'confidence',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'input_snapshot',
            sa.JSON(),
            nullable=True
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
            ['suggestion_id'],
            ['category_suggestions.id']
        ),

        sa.ForeignKeyConstraint(
            ['suggested_category_id'],
            ['business_categories.id']
        ),

        sa.PrimaryKeyConstraint(
            'id'
        )
    )


    op.create_index(
        op.f('ix_category_ai_history_business_id'),
        'category_ai_history',
        ['business_id'],
        unique=False
    )


    op.create_index(
        op.f('ix_category_ai_history_id'),
        'category_ai_history',
        ['id'],
        unique=False
    )


    op.create_index(
        op.f('ix_category_ai_history_suggestion_id'),
        'category_ai_history',
        ['suggestion_id'],
        unique=False
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f('ix_category_ai_history_suggestion_id'),
        table_name='category_ai_history'
    )

    op.drop_index(
        op.f('ix_category_ai_history_id'),
        table_name='category_ai_history'
    )

    op.drop_index(
        op.f('ix_category_ai_history_business_id'),
        table_name='category_ai_history'
    )

    op.drop_table(
        'category_ai_history'
    )