"""add index to secondary phone

Revision ID: 0530a4c58639
Revises: f738cacdbff9
Create Date: 2026-09-28 22:26:49.822117

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0530a4c58639"

down_revision: Union[str, Sequence[str], None] = "f738cacdbff9"

branch_labels = None

depends_on = None



def upgrade() -> None:

    op.create_index(
        op.f("ix_users_secondary_phone"),
        "users",
        ["secondary_phone"],
        unique=False
    )



def downgrade() -> None:

    op.drop_index(
        op.f("ix_users_secondary_phone"),
        table_name="users"
    )