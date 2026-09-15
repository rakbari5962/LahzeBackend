from sqlalchemy.orm import Session

from sqlalchemy import func


from app.models.account import Account

from app.models.reward_event import RewardEvent

from app.models.financial_transaction import FinancialTransaction





# --------------------------------------------------
# موجودی فعلی خزانه پلتفرم
# --------------------------------------------------

def get_treasury_balance(
    db: Session
):

    result = db.query(
        Account.balance
    ).filter(
        Account.account_type == "PLATFORM_TREASURY"
    ).first()


    if not result:

        return 0


    return result[0]





# --------------------------------------------------
# مجموع کمیسیون‌های پرداخت شده
# --------------------------------------------------

def get_total_commission_paid(
    db: Session
):

    result = db.query(
        func.sum(
            RewardEvent.amount
        )
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PROCESSED"
    ).scalar()


    return result or 0





# --------------------------------------------------
# تعداد تراکنش‌های موفق Release
# --------------------------------------------------

def get_transaction_count(
    db: Session
):

    return db.query(
        FinancialTransaction
    ).filter(
        FinancialTransaction.type == "COMMISSION_RELEASE",
        FinancialTransaction.status == "COMPLETED"
    ).count()