from fastapi import APIRouter, Depends, Query
from app.repositories.business_repository import get_business
from app.services.session_service import get_login_session
from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.business_profile import (
    BusinessProfileUpdate
)


from app.schemas.business import (
    BusinessResponse
)


from app.services.business_profile_service import (

    get_business_profile,

    update_profile

)





router = APIRouter(

    prefix="/businesses",

    tags=["Business Profile"]

)








@router.get(

    "/{business_id}/profile",

    response_model=BusinessResponse

)
def read_business_profile(

    business_id: int,

    db: Session = Depends(get_db)

):


    return get_business_profile(

        db=db,

        business_id=business_id

    )



@router.patch(
    "/{business_id}/profile",
    response_model=BusinessResponse
)
def update_business_profile(
    business_id: int,
    data: BusinessProfileUpdate,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    session = get_login_session(
        db=db,
        token=token
    )

    if not session:
        raise Exception("User not logged in")

    business = get_business(
        db=db,
        business_id=business_id
    )

    if not business:
        raise Exception("Business not found")

    if business.owner_user_id != session.user_id:
        raise Exception(
            "You are not the owner of this business"
        )

    if business.is_deleted:
        raise Exception("BUSINESS_DELETED")

    updates = data.model_dump(
        exclude_unset=True
    )

    return update_profile(
        db=db,
        business_id=business_id,
        updates=updates

    )