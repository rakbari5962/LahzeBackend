from sqlalchemy.orm import Session

from app.models.business_referral_share import BusinessReferralShare



def create_share(
    db: Session,
    business_id: int,
    user_id: int,
    role: str,
    percentage: int
):

    share = BusinessReferralShare(
        business_id=business_id,
        user_id=user_id,
        role=role,
        percentage=percentage,
        status="ACTIVE"
    )

    db.add(share)
    db.commit()
    db.refresh(share)

    return share



def get_business_shares(
    db: Session,
    business_id: int
):

    return (
        db.query(BusinessReferralShare)
        .filter(
            BusinessReferralShare.business_id == business_id
        )
        .all()
    )



def get_active_shares(
    db: Session,
    business_id: int
):

    return (
        db.query(BusinessReferralShare)
        .filter(
            BusinessReferralShare.business_id == business_id,
            BusinessReferralShare.status == "ACTIVE"
        )
        .all()
    )



def disable_share(
    db: Session,
    share_id: int
):

    share = (
        db.query(BusinessReferralShare)
        .filter(
            BusinessReferralShare.id == share_id
        )
        .first()
    )

    if share:
        share.status = "DISABLED"
        db.commit()
        db.refresh(share)

    return share