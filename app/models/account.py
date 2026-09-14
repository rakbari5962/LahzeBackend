from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from sqlalchemy.sql import func

from app.database.database import Base



class Account(Base):

    __tablename__ = "accounts"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # نوع مالک حساب
    # USER / BUSINESS / PLATFORM
    owner_type = Column(
        String,
        nullable=False,
        index=True
    )


    # شناسه مالک
    # user_id یا business_id یا platform_id
    owner_id = Column(
        Integer,
        nullable=False,
        index=True
    )


    # نوع حساب مالی
    # CUSTOMER_WALLET
    # BUSINESS_REVENUE
    # PLATFORM_TREASURY
    # REWARD_PAYABLE
    account_type = Column(
        String,
        nullable=False,
        index=True
    )


    # موجودی فعلی حساب
    balance = Column(
        Integer,
        nullable=False,
        default=0
    )


    # واحد پول
    currency = Column(
        String,
        nullable=False,
        default="IRR"
    )


    # وضعیت حساب
    # ACTIVE / BLOCKED
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