from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.reward_event import RewardEvent
from app.models.financial_transaction import FinancialTransaction



# --------------------------------------------------
# دریافت Reward Event های Pending
# --------------------------------------------------

def get_pending_rewards(
    db: Session
):

    return db.query(
        RewardEvent
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PENDING"
    ).order_by(
        RewardEvent.created_at.desc()
    ).all()



# --------------------------------------------------
# تعداد و مبلغ کل Pending ها
# --------------------------------------------------

def get_pending_reward_summary(
    db: Session
):

    result = db.query(
        func.count(RewardEvent.id),
        func.coalesce(
            func.sum(RewardEvent.amount),
            0
        )
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PENDING"
    ).first()


    return {
        "count": result[0],
        "total_amount": result[1]
    }



# --------------------------------------------------
# دریافت Reward های Released شده
# --------------------------------------------------

def get_processed_rewards(
    db: Session
):

    return db.query(
        RewardEvent
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PROCESSED"
    ).order_by(
        RewardEvent.created_at.desc()
    ).all()



# --------------------------------------------------
# خلاصه Released
# --------------------------------------------------

def get_processed_reward_summary(
    db: Session
):

    result = db.query(
        func.count(RewardEvent.id),
        func.coalesce(
            func.sum(RewardEvent.amount),
            0
        )
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PROCESSED"
    ).first()


    return {
        "count": result[0],
        "total_amount": result[1]
    }



# --------------------------------------------------
# دریافت Release های Fail شده
# --------------------------------------------------

def get_failed_release_transactions(
    db: Session
):

    return db.query(
        FinancialTransaction
    ).filter(
        FinancialTransaction.type == "COMMISSION_RELEASE",
        FinancialTransaction.status == "FAILED"
    ).order_by(
        FinancialTransaction.created_at.desc()
    ).all()



# --------------------------------------------------
# خلاصه کلی وضعیت Reward
# --------------------------------------------------

def get_reward_statistics(
    db: Session
):

    pending = get_pending_reward_summary(
        db
    )


    processed = get_processed_reward_summary(
        db
    )


    failed_count = db.query(
        func.count(FinancialTransaction.id)
    ).filter(
        FinancialTransaction.type == "COMMISSION_RELEASE",
        FinancialTransaction.status == "FAILED"
    ).scalar()


    return {

        "pending_count": pending["count"],

        "pending_amount": pending["total_amount"],


        "processed_count": processed["count"],

        "processed_amount": processed["total_amount"],


        "failed_count": failed_count

    }