from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from sqlalchemy.sql import func

from app.database.database import Base



class FinancialTransaction(Base):

    __tablename__ = "financial_transactions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # شناسه یکتا برای عملیات مالی
    # مثال:
    # TX-1001
    transaction_id = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )


    # نوع عملیات مالی
    #
    # DEPOSIT
    # PAYMENT
    # SETTLEMENT
    # REFUND
    # REWARD
    # WITHDRAW
    type = Column(
        String,
        nullable=False,
        index=True
    )


    # وضعیت عملیات
    #
    # PENDING
    # COMPLETED
    # FAILED
    # CANCELLED
    status = Column(
        String,
        nullable=False,
        default="PENDING"
    )


    # مبلغ کل تراکنش
    total_amount = Column(
        Integer,
        nullable=False
    )


    # ارتباط با موجودیت اصلی
    #
    # BOOKING
    # REWARD_EVENT
    # WITHDRAWAL
    reference_type = Column(
        String,
        nullable=False
    )


    reference_id = Column(
        Integer,
        nullable=False,
        index=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )