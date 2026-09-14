from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

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

    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False,
        index=True
    )

    start_time = Column(
        DateTime(timezone=True),
        nullable=False
    )

    end_time = Column(
        DateTime(timezone=True),
        nullable=False
    )

    original_price = Column(
        Integer,
        nullable=False
    )

    discount_percent = Column(
        Integer,
        nullable=False
    )

    final_price = Column(
        Integer,
        nullable=False
    )

    capacity = Column(
        Integer,
        nullable=False,
        default=1
    )

    status = Column(
        String,
        nullable=False,
        default="ACTIVE"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )