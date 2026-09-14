from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base



class LedgerEntry(Base):

    __tablename__ = "ledger_entries"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # حسابی که این تغییر روی آن اتفاق افتاده
    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False,
        index=True
    )


    # شناسه تراکنش گروهی
    # برای اینکه چند Ledger Entry یک عملیات باشند
    transaction_id = Column(
        String,
        nullable=False,
        index=True
    )


    # نوع عملیات مالی
    #
    # DEPOSIT
    # PAYMENT
    # SETTLEMENT
    # REWARD
    # WITHDRAW
    entry_type = Column(
        String,
        nullable=False,
        index=True
    )


    # جهت تغییر
    #
    # CREDIT = افزایش موجودی
    # DEBIT  = کاهش موجودی
    direction = Column(
        String,
        nullable=False
    )


    # مبلغ
    amount = Column(
        Integer,
        nullable=False
    )


    # نوع مرجع
    #
    # BOOKING
    # REVIEW
    # REWARD_EVENT
    # WITHDRAWAL
    reference_type = Column(
        String,
        nullable=False
    )


    # شناسه مرجع
    reference_id = Column(
        Integer,
        nullable=False,
        index=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )