"""add category to businesses

Revision ID: 7063592c1967
Revises: 9c1abaa58bac
Create Date: 2026-09-12 20:32:43.938408

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7063592c1967'
down_revision: Union[str, Sequence[str], None] = '9c1abaa58bac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    # ایجاد جدول خدمات کسب‌وکار
    op.create_table(
        'business_services',

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
            'name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'category',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'duration_minutes',
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            'price',
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            'description',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'is_active',
            sa.Boolean(),
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

        sa.PrimaryKeyConstraint('id')
    )


    op.create_index(
        op.f('ix_business_services_business_id'),
        'business_services',
        ['business_id'],
        unique=False
    )


    op.create_index(
        op.f('ix_business_services_id'),
        'business_services',
        ['id'],
        unique=False
    )


    # اضافه کردن دسته‌بندی به کسب‌وکار
    op.add_column(
        'businesses',
        sa.Column(
            'category_id',
            sa.Integer(),
            nullable=True
        )
    )


    op.create_index(
        op.f('ix_businesses_category_id'),
        'businesses',
        ['category_id'],
        unique=False
    )


    op.create_foreign_key(
        None,
        'businesses',
        'business_categories',
        ['category_id'],
        ['id']
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        None,
        'businesses',
        type_='foreignkey'
    )


    op.drop_index(
        op.f('ix_businesses_category_id'),
        table_name='businesses'
    )


    op.drop_column(
        'businesses',
        'category_id'
    )


    op.drop_index(
        op.f('ix_business_services_id'),
        table_name='business_services'
    )


    op.drop_index(
        op.f('ix_business_services_business_id'),
        table_name='business_services'
    )


    op.drop_table(
        'business_services'
    )