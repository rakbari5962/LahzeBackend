from app.services.wallet_service import create_user_wallet
from app.models.province import Province

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.city import City

from app.schemas.user import (
    UserCreate,
    UserOpportunityProfileUpdate
)





def create_user(
    db: Session,
    user: UserCreate
):

    db_user = User(

        phone_number=user.phone_number,

        province_id=user.province_id,

        city_id=user.city_id

    )


    db.add(db_user)

    db.commit()

    db.refresh(db_user)


    create_user_wallet(
        db,
        db_user.id
    )


    return db_user







def get_user(
    db: Session,
    user_id: int
):

    result = (
        db.query(
            User,
            Province.name.label("province_name"),
            City.name.label("city_name")
        )
        .outerjoin(
            Province,
            User.province_id == Province.id
        )
        .outerjoin(
            City,
            User.city_id == City.id
        )
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not result:
        return None

    user, province_name, city_name = result

    # Response-only attributes
    user.province_name = province_name
    user.city_name = city_name

    print(
        "RETURN USER CHECK:",
        {
            "email": user.email,
            "education": user.education,
            "job_title": user.job_title,
            "bio": user.bio,
            "national_id": user.national_id,
            "province_name": user.province_name,
            "city_name": user.city_name,
        }
    )

    return user







def update_user_city(
    db: Session,
    user_id: int,
    city_id: int,
    province_id: int | None = None
):

    user = db.query(User).filter(

        User.id == user_id

    ).first()



    if not user:

        return None



    user.city_id = city_id



    if province_id is not None:

        user.province_id = province_id



    db.commit()

    db.refresh(user)


    return get_user(
        db,
        user_id
    )







def update_user_profile(
    db: Session,
    user_id: int,
    profile_data: UserOpportunityProfileUpdate
):

    user = db.query(User).filter(

        User.id == user_id

    ).first()



    if not user:

        return None



    user.first_name = profile_data.first_name

    user.secondary_phone = profile_data.secondary_phone

    user.national_id = profile_data.national_id
    
    user.bio = profile_data.bio

    print(
        "BEFORE COMMIT:",
        user.secondary_phone,
        user.national_id,
        user.bio
    )

    user.last_name = profile_data.last_name

    user.gender = profile_data.gender

    user.birth_date = profile_data.birth_date

    user.iban = profile_data.iban

    user.education = profile_data.education

    user.job_title = profile_data.job_title

    user.email = profile_data.email



    user.profile_completed = True



    db.commit()

    db.refresh(user)



    return get_user(
        db,
        user_id
    )