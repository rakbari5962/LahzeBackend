"""add business priority access

Revision ID: db30cd51f754
Revises: 874e33157104
Create Date: 2026-09-16 19:08:52.841016

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "db30cd51f754"

down_revision: Union[str, Sequence[str], None] = "874e33157104"

branch_labels = None

depends_on = None



def upgrade() -> None:

    op.create_table(
        "business_priority_accesses",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "business_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "type",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "source_id",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"]
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    op.create_index(
        "ix_business_priority_accesses_business_id",
        "business_priority_accesses",
        ["business_id"],
        unique=False
    )


    op.create_index(
        "ix_business_priority_accesses_id",
        "business_priority_accesses",
        ["id"],
        unique=False
    )


    op.create_index(
        "ix_business_priority_accesses_user_id",
        "business_priority_accesses",
        ["user_id"],
        unique=False
    )


    op.create_index(
        "unique_first_customer_per_business",
        "business_priority_accesses",
        ["business_id"],
        unique=True,
        postgresql_where=sa.text("type = 'FIRST_CUSTOMER'")
    )





def downgrade() -> None:

    op.drop_index(
        "unique_first_customer_per_business",
        table_name="business_priority_accesses"
    )

    op.drop_index(
        "ix_business_priority_accesses_user_id",
        table_name="business_priority_accesses"
    )

    op.drop_index(
        "ix_business_priority_accesses_id",
        table_name="business_priority_accesses"
    )

    op.drop_index(
        "ix_business_priority_accesses_business_id",
        table_name="business_priority_accesses"
    )


    op.drop_table(
        "business_priority_accesses"
    )