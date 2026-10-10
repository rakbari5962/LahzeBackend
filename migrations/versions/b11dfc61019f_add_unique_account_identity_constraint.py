"""Add a unique identity constraint to financial accounts."""

from alembic import op
import sqlalchemy as sa


revision = "b11dfc61019f"
down_revision = "b7f4c2d91e6a"
branch_labels = None
depends_on = None

CONSTRAINT_NAME = "uq_accounts_owner_type_owner_id_account_type"


def upgrade():
    bind = op.get_bind()

    # Prevent account identities from changing between the preflight check
    # and constraint creation on PostgreSQL.
    if bind.dialect.name == "postgresql":
        bind.execute(sa.text(
            "LOCK TABLE accounts IN ACCESS EXCLUSIVE MODE"
        ))

    duplicates = bind.execute(sa.text("""
        SELECT
            owner_type,
            owner_id,
            account_type,
            COUNT(*) AS row_count
        FROM accounts
        GROUP BY owner_type, owner_id, account_type
        HAVING COUNT(*) > 1
        ORDER BY row_count DESC, owner_type, owner_id, account_type
        LIMIT 20
    """)).mappings().all()

    if duplicates:
        examples = "; ".join(
            (
                f"(owner_type={row['owner_type']!r}, "
                f"owner_id={row['owner_id']}, "
                f"account_type={row['account_type']!r}, "
                f"count={row['row_count']})"
            )
            for row in duplicates
        )
        raise RuntimeError(
            "Cannot add account identity unique constraint: duplicate "
            "account identities exist. Reconcile them manually; no rows "
            "were automatically deleted. Examples: " + examples
        )

    op.create_unique_constraint(
        CONSTRAINT_NAME,
        "accounts",
        ["owner_type", "owner_id", "account_type"],
    )


def downgrade():
    op.drop_constraint(
        CONSTRAINT_NAME,
        "accounts",
        type_="unique",
    )
