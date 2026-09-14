from fastapi import APIRouter, Depends

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

    db: Session = Depends(get_db)

):


    return update_profile(

        db=db,

        business_id=business_id,

        description=data.description,

        phone=data.phone

    )