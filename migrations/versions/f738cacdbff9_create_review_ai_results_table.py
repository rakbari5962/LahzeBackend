"""create review ai results table

Revision ID: f738cacdbff9
Revises: 353cad52793b
Create Date: 2026-09-24 23:39:43.285745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f738cacdbff9'
down_revision: Union[str, Sequence[str], None] = '353cad52793b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'review_ai_results',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'review_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'business_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'topics',
            sa.JSON(),
            nullable=False
        ),

        sa.Column(
            'sentiment',
            sa.JSON(),
            nullable=True
        ),

        sa.Column(
            'raw_response',
            sa.JSON(),
            nullable=True
        ),

        sa.Column(
            'model_version',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['review_id'],
            ['reviews.id']
        ),

        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id']
        ),

        sa.PrimaryKeyConstraint(
            'id'
        )
    )


    op.create_index(
        op.f('ix_review_ai_results_id'),
        'review_ai_results',
        ['id'],
        unique=False
    )


    op.create_index(
        op.f('ix_review_ai_results_review_id'),
        'review_ai_results',
        ['review_id'],
        unique=True
    )


    op.create_index(
        op.f('ix_review_ai_results_business_id'),
        'review_ai_results',
        ['business_id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f('ix_review_ai_results_business_id'),
        table_name='review_ai_results'
    )

    op.drop_index(
        op.f('ix_review_ai_results_review_id'),
        table_name='review_ai_results'
    )

    op.drop_index(
        op.f('ix_review_ai_results_id'),
        table_name='review_ai_results'
    )

    op.drop_table(
        'review_ai_results'
    )