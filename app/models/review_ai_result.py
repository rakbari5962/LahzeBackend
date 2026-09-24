from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    JSON,
    String,
    DateTime
)

from sqlalchemy.sql import func

from app.database.database import Base


class ReviewAIResult(Base):

    __tablename__ = "review_ai_results"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    review_id = Column(
        Integer,
        ForeignKey("reviews.id"),
        nullable=False,
        unique=True,
        index=True
    )


    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        index=True
    )


    topics = Column(
        JSON,
        nullable=False
    )


    sentiment = Column(
        JSON,
        nullable=True
    )


    raw_response = Column(
        JSON,
        nullable=True
    )


    model_version = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )