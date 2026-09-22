from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.database import Base


class Booking(Base):
    __tablename__ = "bookings"

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
        nullable=False,
        index=True
    )

    opportunity_id = Column(
        Integer,
        ForeignKey("opportunities.id"),
        nullable=False,
        index=True
    )

    status = Column(
    String,
    nullable=False,
    default="PENDING_CONFIRMATION"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    confirmed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    cancelled_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    business = relationship(
        "Business"
    )


    opportunity = relationship(
        "Opportunity"
    )