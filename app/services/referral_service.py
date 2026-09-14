from sqlalchemy.orm import Session

from app.repositories.business_referral_share_repository import create_share



def create_business_referral_chain(
    db: Session,
    business_id: int,
    first_referrer_id: int,
    second_referrer_id: int
):

    first_share = create_share(
        db=db,
        business_id=business_id,
        user_id=first_referrer_id,
        role="FOUNDER_LEVEL_1",
        percentage=1
    )


    second_share = create_share(
        db=db,
        business_id=business_id,
        user_id=second_referrer_id,
        role="FOUNDER_LEVEL_2",
        percentage=1
    )


    return [
        first_share,
        second_share
    ]