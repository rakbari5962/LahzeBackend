"""create sessions table

Revision ID: 4ab2815a2cd8
Revises: 6b7460ca63a1
Create Date: 2026-09-17 14:56:40.891733

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4ab2815a2cd8"

down_revision: Union[str, Sequence[str], None] = "6b7460ca63a1"

branch_labels = None

depends_on = None


def upgrade() -> None:

    op.create_table(
        "sessions",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "token",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True
        ),

        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        )
    )


    op.create_index(
        "ix_sessions_user_id",
        "sessions",
        ["user_id"],
        unique=False
    )


    op.create_index(
        "ix_sessions_token",
        "sessions",
        ["token"],
        unique=True
    )



def downgrade() -> None:

    op.drop_index(
        "ix_sessions_token",
        table_name="sessions"
    )


    op.drop_index(
        "ix_sessions_user_id",
        table_name="sessions"
    )


    op.drop_table(
        "sessions"
    )