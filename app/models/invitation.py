from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
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


    # Phone number of invited business owner
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


    # True only when accepted user's phone
    # matches the invited phone number
    #
    # True:
    #   owner_phone == accepted_user.phone_number
    #
    # False:
    #   someone else used the invitation link
    accepted_phone_match = Column(
        Boolean,
        nullable=False,
        default=False
    )


    accepted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )