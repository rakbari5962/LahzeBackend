from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base



class BusinessReferralShare(Base):

    __tablename__ = "business_referral_shares"


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


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )


    role = Column(
        String,
        nullable=False
    )


    percentage = Column(
        Integer,
        nullable=False
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