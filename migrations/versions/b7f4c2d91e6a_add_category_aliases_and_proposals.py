"""add managed category aliases and quarantined proposals

Revision ID: b7f4c2d91e6a
Revises: 0530a4c58639
Create Date: 2026-10-09 00:00:00.000000
"""

import re
import unicodedata
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7f4c2d91e6a"
down_revision: Union[str, Sequence[str], None] = "0530a4c58639"
branch_labels = None
depends_on = None


def _normalize(value: str | None) -> str:
    # Frozen copy of app.services.category_normalization.normalize_category_text;
    # migrations must not import application code that may change later.
    table = str.maketrans({
        "ي": "ی", "ى": "ی", "ك": "ک",
        "ۀ": "ه", "ة": "ه", "ؤ": "و",
        "أ": "ا", "إ": "ا", "ٱ": "ا",
    })
    text = unicodedata.normalize("NFKC", value or "").translate(table)
    text = re.sub("[‌‍‎‏ـ​﻿]", " ", text)
    text = re.sub("[ً-ٰٟ]", "", text)
    text = re.sub(r"[^\w\s]", " ", text.replace("_", " "), flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip().casefold()


def upgrade() -> None:
    op.add_column("business_categories", sa.Column("normalized_name", sa.String(), nullable=True))

    bind = op.get_bind()
    rows = bind.execute(sa.text("SELECT id, name FROM business_categories")).mappings().all()
    normalized: dict[str, int] = {}
    for row in rows:
        identity = _normalize(row["name"])
        if identity in normalized and normalized[identity] != row["id"]:
            raise RuntimeError(
                "Cannot add category name uniqueness; normalized collision between "
                f"business_categories {normalized[identity]} and {row['id']} ({identity!r})."
            )
        normalized[identity] = row["id"]
        bind.execute(
            sa.text("UPDATE business_categories SET normalized_name = :identity WHERE id = :id"),
            {"identity": identity, "id": row["id"]},
        )

    op.create_index(
        "uq_business_categories_normalized_name",
        "business_categories",
        ["normalized_name"],
        unique=True,
    )

    op.create_table(
        "business_category_aliases",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("alias", sa.String(), nullable=False),
        sa.Column("normalized_alias", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["business_categories.id"]),
        sa.UniqueConstraint("normalized_alias", name="uq_business_category_alias_normalized"),
    )
    op.create_index("ix_business_category_aliases_id", "business_category_aliases", ["id"])
    op.create_index("ix_business_category_aliases_category_id", "business_category_aliases", ["category_id"])

    op.create_table(
        "category_proposals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("normalized_title", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("final_category_id", sa.Integer(), nullable=True),
        sa.Column("reviewed_by_user_id", sa.Integer(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("review_note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["final_category_id"], ["business_categories.id"]),
        sa.ForeignKeyConstraint(["reviewed_by_user_id"], ["users.id"]),
    )
    op.create_index("ix_category_proposals_id", "category_proposals", ["id"])
    op.create_index("ix_category_proposals_normalized_title", "category_proposals", ["normalized_title"])
    op.create_index(
        "uq_category_proposals_pending_title",
        "category_proposals",
        ["normalized_title"],
        unique=True,
        postgresql_where=sa.text("status = 'PENDING'"),
    )

    op.create_table(
        "category_proposal_businesses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("proposal_id", sa.Integer(), nullable=False),
        sa.Column("business_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["proposal_id"], ["category_proposals.id"]),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"]),
        sa.UniqueConstraint("proposal_id", "business_id", name="uq_category_proposal_business"),
    )
    op.create_index("ix_category_proposal_businesses_id", "category_proposal_businesses", ["id"])
    op.create_index("ix_category_proposal_businesses_proposal_id", "category_proposal_businesses", ["proposal_id"])
    op.create_index("ix_category_proposal_businesses_business_id", "category_proposal_businesses", ["business_id"])

    op.create_table(
        "category_proposal_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("proposal_id", sa.Integer(), nullable=False),
        sa.Column("original_title", sa.String(), nullable=False),
        sa.Column("from_status", sa.String(), nullable=False),
        sa.Column("to_status", sa.String(), nullable=False),
        sa.Column("decision", sa.String(), nullable=False),
        sa.Column("admin_user_id", sa.Integer(), nullable=True),
        sa.Column("replacement_title", sa.String(), nullable=True),
        sa.Column("final_category_id", sa.Integer(), nullable=True),
        sa.Column("note", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["proposal_id"], ["category_proposals.id"]),
        sa.ForeignKeyConstraint(["admin_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["final_category_id"], ["business_categories.id"]),
    )
    op.create_index("ix_category_proposal_history_id", "category_proposal_history", ["id"])
    op.create_index("ix_category_proposal_history_proposal_id", "category_proposal_history", ["proposal_id"])

    health = bind.execute(
        sa.text("SELECT id FROM business_categories WHERE slug = 'health' AND is_active = true")
    ).scalar_one_or_none()
    if health is not None:
        bind.execute(
            sa.text(
                "INSERT INTO business_category_aliases "
                "(category_id, alias, normalized_alias) VALUES (:category_id, :alias, :normalized_alias) "
                "ON CONFLICT (normalized_alias) DO NOTHING"
            ),
            {"category_id": health, "alias": "Psychologist", "normalized_alias": "psychologist"},
        )


def downgrade() -> None:
    op.drop_index("ix_category_proposal_history_proposal_id", table_name="category_proposal_history")
    op.drop_index("ix_category_proposal_history_id", table_name="category_proposal_history")
    op.drop_table("category_proposal_history")
    op.drop_index("ix_category_proposal_businesses_business_id", table_name="category_proposal_businesses")
    op.drop_index("ix_category_proposal_businesses_proposal_id", table_name="category_proposal_businesses")
    op.drop_index("ix_category_proposal_businesses_id", table_name="category_proposal_businesses")
    op.drop_table("category_proposal_businesses")
    op.drop_index("uq_category_proposals_pending_title", table_name="category_proposals")
    op.drop_index("ix_category_proposals_normalized_title", table_name="category_proposals")
    op.drop_index("ix_category_proposals_id", table_name="category_proposals")
    op.drop_table("category_proposals")
    op.drop_index("ix_business_category_aliases_category_id", table_name="business_category_aliases")
    op.drop_index("ix_business_category_aliases_id", table_name="business_category_aliases")
    op.drop_table("business_category_aliases")
    op.drop_index("uq_business_categories_normalized_name", table_name="business_categories")
    op.drop_column("business_categories", "normalized_name")
