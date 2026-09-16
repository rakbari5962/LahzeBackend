from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base



class BusinessPriorityAccess(Base):

    __tablename__ = "business_priority_accesses"


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


    # FOUNDER_INVITER
    # FIRST_CUSTOMER
    type = Column(
        String,
        nullable=False
    )


    # برای اینکه بدانیم این امتیاز از کجا آمده
    #
    # Invitation id
    # Booking id
    source_id = Column(
        Integer,
        nullable=True
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