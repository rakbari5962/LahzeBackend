"""create business ai narratives table

Revision ID: 98444fd7fe48
Revises: 4d35d3510889
Create Date: 2026-09-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "98444fd7fe48"

down_revision: Union[str, Sequence[str], None] = "4d35d3510889"

branch_labels = None

depends_on = None



def upgrade() -> None:

    op.create_table(

        "business_ai_narratives",

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
            "summary",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "positive_summary",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "improvement_summary",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "trust_score",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "model_version",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"]
        )
    )


    op.create_index(

        "ix_business_ai_narratives_business_id",

        "business_ai_narratives",

        ["business_id"]

    )




def downgrade() -> None:

    op.drop_index(

        "ix_business_ai_narratives_business_id",

        table_name="business_ai_narratives"

    )


    op.drop_table(
        "business_ai_narratives"
    )