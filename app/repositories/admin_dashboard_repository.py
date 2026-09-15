from sqlalchemy.orm import Session

from sqlalchemy import func

from app.models.reward_event import RewardEvent

from app.models.business_referral_share import BusinessReferralShare





def get_total_paid_commission(
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





def get_total_releases(
    db: Session
):

    return db.query(
        RewardEvent
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PROCESSED"
    ).count()





def get_pending_commissions(
    db: Session
):

    return db.query(
        RewardEvent
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PENDING"
    ).count()





def get_failed_commissions(
    db: Session
):

    return db.query(
        RewardEvent
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "FAILED"
    ).count()





def get_active_referrers(
    db: Session
):

    return db.query(
        BusinessReferralShare.user_id
    ).filter(
        BusinessReferralShare.status == "ACTIVE"
    ).distinct().count()



def get_earning_referrers(
    db: Session
):

    return db.query(
        RewardEvent.user_id
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PROCESSED"
    ).distinct().count()