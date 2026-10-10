from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint,
    text
)

from sqlalchemy.sql import func

from app.database.database import Base


PROPOSAL_PENDING = "PENDING"
PROPOSAL_APPROVED = "APPROVED"
PROPOSAL_REJECTED_REPLACED = "REJECTED_REPLACED"


class CategoryProposal(Base):
    """A proposed NEW category title, quarantined until an admin decides.

    Separate from `category_suggestions`, which can only reference an
    already-existing category.
    """

    __tablename__ = "category_proposals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Original title as proposed. Never overwritten by a decision.
    title = Column(
        String,
        nullable=False
    )

    normalized_title = Column(
        String,
        nullable=False,
        index=True
    )

    source = Column(
        String,
        nullable=False,
        default="LLM"
    )

    status = Column(
        String,
        nullable=False,
        default=PROPOSAL_PENDING
    )

    final_category_id = Column(
        Integer,
        ForeignKey("business_categories.id"),
        nullable=True
    )

    reviewed_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    reviewed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    review_note = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    __table_args__ = (
        # Concurrency-safe dedup: only one PENDING proposal per identity.
        Index(
            "uq_category_proposals_pending_title",
            "normalized_title",
            unique=True,
            postgresql_where=text("status = 'PENDING'"),
            sqlite_where=text("status = 'PENDING'")
        ),
    )


class CategoryProposalBusiness(Base):

    __tablename__ = "category_proposal_businesses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    proposal_id = Column(
        Integer,
        ForeignKey("category_proposals.id"),
        nullable=False,
        index=True
    )

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "proposal_id",
            "business_id",
            name="uq_category_proposal_business"
        ),
    )


class CategoryProposalHistory(Base):

    __tablename__ = "category_proposal_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    proposal_id = Column(
        Integer,
        ForeignKey("category_proposals.id"),
        nullable=False,
        index=True
    )

    original_title = Column(
        String,
        nullable=False
    )

    from_status = Column(
        String,
        nullable=False
    )

    to_status = Column(
        String,
        nullable=False
    )

    # APPROVED | REJECTED_WITH_REPLACEMENT
    decision = Column(
        String,
        nullable=False
    )

    admin_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    replacement_title = Column(
        String,
        nullable=True
    )

    final_category_id = Column(
        Integer,
        ForeignKey("business_categories.id"),
        nullable=True
    )

    note = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
