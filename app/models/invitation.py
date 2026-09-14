from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # User who invited the business
    inviter_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Phone number of business owner
    owner_phone = Column(
        String,
        nullable=False,
        index=True
    )

    # Suggested business name
    business_name = Column(
        String,
        nullable=True
    )

    city = Column(
        String,
        nullable=True
    )

    # PENDING / ACCEPTED / EXPIRED
    status = Column(
        String,
        default="PENDING"
    )

    # User who accepted invitation after registration
    accepted_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    accepted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )