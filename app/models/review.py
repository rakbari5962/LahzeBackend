from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.sql import func

from app.database.database import Base


class Review(Base):

    __tablename__ = "reviews"


    __table_args__ = (
        UniqueConstraint(
            "booking_id",
            name="unique_booking_review"
        ),
    )


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
        index=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )


    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        index=True
    )


    rating = Column(
        Integer,
        nullable=False
    )


    comment = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )