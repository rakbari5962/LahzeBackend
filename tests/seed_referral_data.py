import app.models

from app.database.database import SessionLocal

from app.models.user import User
from app.models.business import Business


db = SessionLocal()


try:

    # Create Nazanin

    nazanin = User(
        phone_number="09120000001"
    )


    # Create Sara

    sara = User(
        phone_number="09120000002"
    )


    # Create Business Owner

    business_owner = User(
        phone_number="09120000003"
    )


    db.add(nazanin)
    db.add(sara)
    db.add(business_owner)

    db.commit()


    db.refresh(nazanin)
    db.refresh(sara)
    db.refresh(business_owner)



    # Create Atrin Salon

    business = Business(
        owner_user_id=business_owner.id,
        name="Atrin Salon"
    )


    db.add(business)

    db.commit()

    db.refresh(business)



    print("CREATED TEST DATA")

    print("-------------------")

    print(
        "Nazanin ID:",
        nazanin.id
    )

    print(
        "Sara ID:",
        sara.id
    )

    print(
        "Business Owner ID:",
        business_owner.id
    )

    print(
        "Business ID:",
        business.id
    )


finally:

    db.close()