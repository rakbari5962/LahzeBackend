from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.services.wallet_service import get_or_create_user_wallet
from app.services.account_balance_service import get_account_balance

from app.repositories.wallet_hold_repository import (
    create_hold,
    get_active_hold,
    release_hold,
    capture_hold
)

from app.models.wallet_hold import WalletHold



def get_user_active_holds_amount(
    db: Session,
    user_id: int
):
    """
    مجموع مبلغ‌هایی که فعلا در رزروهای در انتظار تایید بلوکه شده‌اند
    """

    holds = db.query(WalletHold).filter(
        WalletHold.user_id == user_id,
        WalletHold.status == "ACTIVE"
    ).all()


    total = 0


    for hold in holds:
        total += hold.amount


    return total





def get_available_wallet_balance(
    db: Session,
    user_id: int
):
    """
    موجودی قابل استفاده مشتری
    = موجودی کیف پول - مبلغ‌های بلوکه شده
    """


    wallet = get_or_create_user_wallet(
        db,
        user_id
    )


    if not wallet:
        return 0



    active_holds = get_user_active_holds_amount(
        db,
        user_id
    )


    return wallet.balance - active_holds





def create_booking_hold(
    db: Session,
    user_id: int,
    booking_id: int,
    amount: int
):
    """
    هنگام درخواست رزرو فرصت لحظه‌ای
    پول فقط بلوکه می‌شود
    و هنوز به Escrow منتقل نمی‌شود
    """


    if amount <= 0:
        return None



    available_balance = get_available_wallet_balance(
        db,
        user_id
    )


    if available_balance < amount:

        return None



    existing_hold = get_active_hold(
        db,
        booking_id
    )


    if existing_hold:

        return existing_hold



    return create_hold(
        db=db,
        user_id=user_id,
        booking_id=booking_id,
        amount=amount
    )





def release_booking_hold(
    db: Session,
    booking_id: int
):
    """
    وقتی:
    - مشتری قبل از تایید لغو کند
    - Deadline تمام شود

    مبلغ آزاد می‌شود
    """


    return release_hold(
        db,
        booking_id
    )





def capture_booking_hold(
    db: Session,
    booking_id: int
):
    """
    وقتی سالن تایید کرد:

    Hold:
    ACTIVE

    تبدیل می‌شود به:

    CAPTURED

    سپس Payment انجام می‌شود
    """


    return capture_hold(
        db,
        booking_id
    )