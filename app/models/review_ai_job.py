from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.sql import func

from app.database.database import Base


class ReviewAIJob(Base):

    __tablename__ = "review_ai_jobs"


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


    status = Column(
        String,
        nullable=False,
        default="pending"
    )


    retry_count = Column(
        Integer,
        nullable=False,
        default=0
    )


    last_error = Column(
        Text,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    processed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )