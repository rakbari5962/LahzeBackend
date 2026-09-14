from app.database.database import SessionLocal

from app.models.business_referral_share import BusinessReferralShare



db = SessionLocal()



shares = [

    BusinessReferralShare(
        business_id=3,
        user_id=7,
        role="FOUNDER_LEVEL_1",
        percentage=1,
        status="ACTIVE"
    ),


    BusinessReferralShare(
        business_id=3,
        user_id=8,
        role="FOUNDER_LEVEL_2",
        percentage=1,
        status="ACTIVE"
    )

]



for share in shares:
    db.add(share)



db.commit()



print("BUSINESS REFERRAL SHARES CREATED")
print("----------------------------------")
print("Business: 3")
print("User 7: 1%")
print("User 8: 1%")



db.close()