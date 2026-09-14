from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.business_completion import (
    BusinessCompletionResponse
)


from app.services.business_completion_service import (
    calculate_business_completion
)





router = APIRouter(

    prefix="/businesses",

    tags=["Business Completion"]

)







@router.get(

    "/{business_id}/completion",

    response_model=BusinessCompletionResponse

)
def get_business_completion(

    business_id: int,

    db: Session = Depends(get_db)

):


    return calculate_business_completion(

        db=db,

        business_id=business_id

    )