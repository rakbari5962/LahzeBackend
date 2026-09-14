from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

from app.database.database import Base


class Service(Base):
    __tablename__ = "services"

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

    name = Column(
        String,
        nullable=False
    )

    base_price = Column(
        Integer,
        nullable=False
    )

    duration_minutes = Column(
        Integer,
        nullable=False
    )

    active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )