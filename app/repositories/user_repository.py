from app.services.wallet_service import create_user_wallet
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate



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

    return db.query(User).filter(

        User.id == user_id

    ).first()





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


    return user