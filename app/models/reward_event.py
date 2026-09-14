from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy import DateTime

from app.database.database import Base


class RewardEvent(Base):

    __tablename__ = "reward_events"


    id = Column(
        Integer,
        primary_key=True,
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
        nullable=True,
        index=True
    )


    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=True,
        index=True
    )

    review_id = Column(
    Integer,
    ForeignKey("reviews.id"),
    nullable=True,
    index=True
    )

    transaction_id = Column(
        String,
        nullable=True,
        index=True
    )


    # جلوگیری از پرداخت تکراری
    # مثال:
    # SETTLE-1001-2-4-REFERRAL_REWARD

    idempotency_key = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )


    type = Column(
        String,
        nullable=False
    )


    amount = Column(
        Integer,
        nullable=False
    )


    status = Column(
        String,
        nullable=False,
        default="PENDING"
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )