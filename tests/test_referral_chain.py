import app.models

from app.database.database import SessionLocal

from app.services.referral_service import create_business_referral_chain

from app.models.business_referral_share import BusinessReferralShare



db = SessionLocal()


try:

    shares = create_business_referral_chain(
        db=db,
        business_id=2,
        first_referrer_id=4,
        second_referrer_id=5
    )


    print("REFERRAL SHARES CREATED")
    print("-----------------------")


    for share in shares:

        print(
            "ID:",
            share.id,
            "| Business:",
            share.business_id,
            "| User:",
            share.user_id,
            "| Role:",
            share.role,
            "| Percentage:",
            share.percentage,
            "| Status:",
            share.status
        )


finally:

    db.close()