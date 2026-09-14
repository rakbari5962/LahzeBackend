from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.services.business_visibility_service import (
    get_business_visibility_detail
)





router = APIRouter(

    prefix="/businesses",

    tags=["Business Visibility"]

)







@router.get(

    "/{business_id}/visibility"

)
def check_business_visibility(

    business_id: int,

    db: Session = Depends(get_db)

):


    return get_business_visibility_detail(

        db=db,

        business_id=business_id

    )