from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base



class ReviewRequest(Base):

    __tablename__ = "review_requests"


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


    status = Column(
        String,
        nullable=False,
        default="PENDING"
    )


    sent_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )