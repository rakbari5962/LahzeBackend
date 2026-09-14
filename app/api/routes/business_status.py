from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.business_status import (
    BusinessStatusUpdate
)


from app.schemas.business import (
    BusinessResponse
)


from app.services.business_status_management_service import (
    update_business_status_manually
)





router = APIRouter(

    prefix="/businesses",

    tags=["Business Status"]

)








@router.patch(

    "/{business_id}/status",

    response_model=BusinessResponse

)
def update_status(

    business_id: int,

    data: BusinessStatusUpdate,

    db: Session = Depends(get_db)

):


    return update_business_status_manually(

        db=db,

        business_id=business_id,

        status=data.status

    )