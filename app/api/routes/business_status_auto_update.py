from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.services.business_status_auto_update_service import (
    auto_update_business_status
)





router = APIRouter(

    prefix="/businesses",

    tags=["Business Status Auto Update"]

)







@router.post(

    "/{business_id}/status/auto-update"

)
def auto_update_status(

    business_id: int,

    db: Session = Depends(get_db)

):


    return auto_update_business_status(

        db=db,

        business_id=business_id

    )