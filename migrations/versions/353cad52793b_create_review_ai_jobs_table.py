"""create review ai jobs table

Revision ID: 353cad52793b
Revises: c4e448e36f9b
Create Date: 2026-09-24 21:48:44.995848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '353cad52793b'
down_revision: Union[str, Sequence[str], None] = 'c4e448e36f9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'review_ai_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('review_id', sa.Integer(), nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('retry_count', sa.Integer(), nullable=False),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),
        sa.Column(
            'processed_at',
            sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id']
        ),
        sa.ForeignKeyConstraint(
            ['review_id'],
            ['reviews.id']
        ),
        sa.PrimaryKeyConstraint('id')
    )


    op.create_index(
        op.f('ix_review_ai_jobs_business_id'),
        'review_ai_jobs',
        ['business_id'],
        unique=False
    )


    op.create_index(
        op.f('ix_review_ai_jobs_id'),
        'review_ai_jobs',
        ['id'],
        unique=False
    )


    op.create_index(
        op.f('ix_review_ai_jobs_review_id'),
        'review_ai_jobs',
        ['review_id'],
        unique=True
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f('ix_review_ai_jobs_review_id'),
        table_name='review_ai_jobs'
    )

    op.drop_index(
        op.f('ix_review_ai_jobs_id'),
        table_name='review_ai_jobs'
    )

    op.drop_index(
        op.f('ix_review_ai_jobs_business_id'),
        table_name='review_ai_jobs'
    )

    op.drop_table('review_ai_jobs')
