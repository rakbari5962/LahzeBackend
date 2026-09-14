from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class WalletHold(Base):

    __tablename__ = "wallet_holds"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )


    booking_id = Column(
        Integer,
        nullable=False,
        index=True
    )


    amount = Column(
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


    released_at = Column(
        DateTime(timezone=True),
        nullable=True
    )