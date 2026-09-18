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



class ReviewAIAnalysis(Base):

    __tablename__ = "review_ai_analysis"


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


    total_reviews = Column(
        Integer,
        nullable=False,
        default=0
    )


    average_rating = Column(
        String,
        nullable=True
    )


    strengths = Column(
        JSON,
        nullable=True
    )


    weaknesses = Column(
        JSON,
        nullable=True
    )


    themes = Column(
        JSON,
        nullable=True
    )


    # تحلیل احساسات به تفکیک موضوع
    topic_sentiment = Column(
        JSON,
        nullable=True
    )


    customer_sentiment = Column(
        JSON,
        nullable=True
    )


    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    model_version = Column(
        String,
        nullable=True
    )