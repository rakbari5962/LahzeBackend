from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint
)

from app.database.database import Base



class BusinessAttributeScore(Base):

    __tablename__ = "business_attribute_scores"


    __table_args__ = (
        UniqueConstraint(
            "business_id",
            "attribute_id",
            name="unique_business_attribute_score"
        ),
    )


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


    attribute_id = Column(
        Integer,
        ForeignKey("review_attributes.id"),
        nullable=False,
        index=True
    )


    positive_count = Column(
        Integer,
        nullable=False,
        default=0
    )


    negative_count = Column(
        Integer,
        nullable=False,
        default=0
    )