"""create no show reports table

Revision ID: 0825d17c2d36
Revises: db30cd51f754
Create Date: 2026-09-17

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0825d17c2d36"

down_revision: Union[str, Sequence[str], None] = "db30cd51f754"

branch_labels = None

depends_on = None



def upgrade() -> None:


    op.create_table(
        "no_show_reports",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "booking_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "business_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "reported_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True
        ),

        sa.Column(
            "customer_response_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),

        sa.Column(
            "resolved_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),


        sa.ForeignKeyConstraint(
            ["booking_id"],
            ["bookings.id"]
        ),

        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )



    op.create_index(
        "ix_no_show_reports_booking_id",
        "no_show_reports",
        ["booking_id"],
        unique=False
    )


    op.create_index(
        "ix_no_show_reports_business_id",
        "no_show_reports",
        ["business_id"],
        unique=False
    )





def downgrade() -> None:


    op.drop_index(
        "ix_no_show_reports_business_id",
        table_name="no_show_reports"
    )


    op.drop_index(
        "ix_no_show_reports_booking_id",
        table_name="no_show_reports"
    )


    op.drop_table(
        "no_show_reports"
    )