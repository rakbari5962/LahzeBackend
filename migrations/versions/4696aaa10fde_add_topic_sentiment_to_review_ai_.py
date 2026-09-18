"""add topic sentiment to review ai analysis

Revision ID: 4696aaa10fde
Revises: 98444fd7fe48
Create Date: 2026-09-18
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4696aaa10fde"

down_revision: Union[str, Sequence[str], None] = "98444fd7fe48"

branch_labels = None

depends_on = None



def upgrade() -> None:

    op.add_column(

        "review_ai_analysis",

        sa.Column(

            "topic_sentiment",

            sa.JSON(),

            nullable=True

        )

    )



def downgrade() -> None:

    op.drop_column(

        "review_ai_analysis",

        "topic_sentiment"

    )