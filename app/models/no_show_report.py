from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base



class NoShowReport(Base):

    __tablename__ = "no_show_reports"


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


    reported_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    customer_response_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )