from sqlalchemy.orm import Session


from app.models.business import Business


from app.schemas.business import BusinessCreate







def create_business(

    db: Session,

    business: BusinessCreate,

    owner_user_id: int

):


    db_business = Business(

        name=business.name,

        owner_user_id=owner_user_id,

        province_id=business.province_id,

        city_id=business.city_id,

        description=business.description,

        phone=business.phone

    )


    db.add(db_business)

    db.commit()

    db.refresh(db_business)


    return db_business










def get_business(

    db: Session,

    business_id: int

):


    return db.query(Business).filter(

        Business.id == business_id

    ).first()










def update_business_location(

    db: Session,

    business_id: int,

    latitude: float,

    longitude: float,

    address: str | None = None

):


    business = db.query(Business).filter(

        Business.id == business_id

    ).first()



    if not business:

        return None



    business.latitude = latitude

    business.longitude = longitude

    business.address = address



    db.commit()

    db.refresh(business)



    return business










def update_business_profile(

    db: Session,

    business_id: int,

    description: str | None = None,

    phone: str | None = None

):


    business = db.query(Business).filter(

        Business.id == business_id

    ).first()



    if not business:

        return None



    business.description = description

    business.phone = phone



    db.commit()

    db.refresh(business)



    return business