from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base



class BusinessAINarrative(Base):

    __tablename__ = "business_ai_narratives"


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


    summary = Column(
        String,
        nullable=False
    )


    positive_summary = Column(
        String,
        nullable=True
    )


    improvement_summary = Column(
        String,
        nullable=True
    )


    trust_score = Column(
        Integer,
        nullable=True
    )


    model_version = Column(
        String,
        nullable=True
    )


    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )