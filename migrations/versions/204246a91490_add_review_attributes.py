"""add review attributes

Revision ID: 204246a91490
Revises: 4696aaa10fde
Create Date: 2026-09-19 19:32:08.915438

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '204246a91490'

down_revision: Union[str, Sequence[str], None] = '4696aaa10fde'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:

    op.create_table(
        'review_attributes',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'key',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'label',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'category',
            sa.String(),
            nullable=True
        ),

        sa.PrimaryKeyConstraint(
            'id'
        )
    )


    op.create_index(
        op.f('ix_review_attributes_id'),
        'review_attributes',
        ['id'],
        unique=False
    )


    op.create_index(
        op.f('ix_review_attributes_key'),
        'review_attributes',
        ['key'],
        unique=True
    )



    op.create_table(
        'business_attribute_scores',

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
            'attribute_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'positive_count',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'negative_count',
            sa.Integer(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ['attribute_id'],
            ['review_attributes.id']
        ),

        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id']
        ),

        sa.PrimaryKeyConstraint(
            'id'
        ),

        sa.UniqueConstraint(
            'business_id',
            'attribute_id',
            name='unique_business_attribute_score'
        )
    )


    op.create_index(
        op.f('ix_business_attribute_scores_attribute_id'),
        'business_attribute_scores',
        ['attribute_id'],
        unique=False
    )


    op.create_index(
        op.f('ix_business_attribute_scores_business_id'),
        'business_attribute_scores',
        ['business_id'],
        unique=False
    )


    op.create_index(
        op.f('ix_business_attribute_scores_id'),
        'business_attribute_scores',
        ['id'],
        unique=False
    )



def downgrade() -> None:

    op.drop_index(
        op.f('ix_business_attribute_scores_id'),
        table_name='business_attribute_scores'
    )


    op.drop_index(
        op.f('ix_business_attribute_scores_business_id'),
        table_name='business_attribute_scores'
    )


    op.drop_index(
        op.f('ix_business_attribute_scores_attribute_id'),
        table_name='business_attribute_scores'
    )


    op.drop_table(
        'business_attribute_scores'
    )


    op.drop_index(
        op.f('ix_review_attributes_key'),
        table_name='review_attributes'
    )


    op.drop_index(
        op.f('ix_review_attributes_id'),
        table_name='review_attributes'
    )


    op.drop_table(
        'review_attributes'
    )