from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.database.database import Base



class ReviewAttribute(Base):

    __tablename__ = "review_attributes"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    key = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )


    label = Column(
        String,
        nullable=False
    )


    category = Column(
        String,
        nullable=True
    )