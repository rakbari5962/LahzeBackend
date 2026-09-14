from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON
)

from sqlalchemy.sql import func

from app.database.database import Base


class CategorySuggestion(Base):

    __tablename__ = "category_suggestions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        index=True
    )


    suggested_category_id = Column(
        Integer,
        ForeignKey("business_categories.id"),
        nullable=False,
        index=True
    )


    confidence = Column(
        Integer,
        nullable=False
    )


    reason = Column(
        String,
        nullable=True
    )


    status = Column(
        String,
        nullable=False,
        default="PENDING"
    )


    input_snapshot = Column(
        JSON,
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