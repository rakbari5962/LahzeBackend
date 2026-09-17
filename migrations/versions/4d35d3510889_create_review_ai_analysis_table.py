"""create review ai analysis table

Revision ID: 4d35d3510889
Revises: 0825d17c2d36
Create Date: 2026-09-17 18:41:35.812258

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4d35d3510889'
down_revision: Union[str, Sequence[str], None] = '0825d17c2d36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:

    op.create_table(
        'review_ai_analysis',

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
            'total_reviews',
            sa.Integer(),
            nullable=False,
            server_default="0"
        ),

        sa.Column(
            'average_rating',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'strengths',
            sa.JSON(),
            nullable=True
        ),

        sa.Column(
            'weaknesses',
            sa.JSON(),
            nullable=True
        ),

        sa.Column(
            'themes',
            sa.JSON(),
            nullable=True
        ),

        sa.Column(
            'customer_sentiment',
            sa.JSON(),
            nullable=True
        ),

        sa.Column(
            'generated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),

        sa.Column(
            'model_version',
            sa.String(),
            nullable=True
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
        'ix_review_ai_analysis_id',
        'review_ai_analysis',
        ['id'],
        unique=False
    )


    op.create_index(
        'ix_review_ai_analysis_business_id',
        'review_ai_analysis',
        ['business_id'],
        unique=False
    )



def downgrade() -> None:
    op.drop_table(
        'review_ai_analysis'
    )

    op.drop_index(
        'ix_review_ai_analysis_id',
        table_name='review_ai_analysis'
    )

    op.drop_table(
        'review_ai_analysis'
    )