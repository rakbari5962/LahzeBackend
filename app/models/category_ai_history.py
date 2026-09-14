from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base



class CategoryAIHistory(Base):

    __tablename__ = "category_ai_history"


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


    suggestion_id = Column(
        Integer,
        ForeignKey("category_suggestions.id"),
        nullable=False,
        index=True
    )


    suggested_category_id = Column(
        Integer,
        ForeignKey("business_categories.id"),
        nullable=False
    )


    action = Column(
        String,
        nullable=False
    )
    # ACCEPTED
    # REJECTED


    confidence = Column(
        Integer,
        nullable=False
    )


    input_snapshot = Column(
        JSON,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )