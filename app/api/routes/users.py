from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserCityUpdate,
    UserOpportunityProfileUpdate
)


from app.repositories.user_repository import (
    create_user,
    get_user,
    update_user_city,
    update_user_profile
)


from app.services.session_service import (
    get_login_session
)





router = APIRouter(

    prefix="/users",

    tags=["Users"]

)









@router.post(

    "/",

    response_model=UserResponse

)
def create_new_user(

    user: UserCreate,

    db: Session = Depends(get_db)

):

    return create_user(

        db,

        user

    )











@router.get(

    "/me",

    response_model=UserResponse

)
def read_current_user(

    token: str,

    db: Session = Depends(get_db)

):


    session = get_login_session(

        db=db,

        token=token

    )


    if not session:

        raise Exception(

            "User not logged in"

        )



    return get_user(

        db,

        session.user_id

    )









@router.patch(

    "/me/city",

    response_model=UserResponse

)
def update_current_user_city(

    city_data: UserCityUpdate,

    token: str,

    db: Session = Depends(get_db)

):


    session = get_login_session(

        db=db,

        token=token

    )


    if not session:

        raise Exception(

            "User not logged in"

        )




    updated_user = update_user_city(

        db=db,

        user_id=session.user_id,

        city_id=city_data.city_id,

        province_id=city_data.province_id

    )



    if not updated_user:

        raise Exception(

            "User not found"

        )



    return updated_user










@router.patch(

    "/me/profile",

    response_model=UserResponse

)
def update_current_user_profile(

    profile_data: UserOpportunityProfileUpdate,

    token: str,

    db: Session = Depends(get_db)

):


    session = get_login_session(

        db=db,

        token=token

    )


    if not session:

        raise Exception(

            "User not logged in"

        )



    updated_user = update_user_profile(

        db=db,

        user_id=session.user_id,

        profile_data=profile_data

    )



    if not updated_user:

        raise Exception(

            "User not found"

        )



    return updated_user











@router.get(

    "/{user_id}",

    response_model=UserResponse

)
def read_user(

    user_id: int,

    db: Session = Depends(get_db)

):

    return get_user(

        db,

        user_id

    )