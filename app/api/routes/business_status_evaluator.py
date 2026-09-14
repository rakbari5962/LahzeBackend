from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.services.business_status_evaluator_service import (
    evaluate_business_status
)





router = APIRouter(

    prefix="/businesses",

    tags=["Business Status Evaluator"]

)







@router.get(

    "/{business_id}/status/evaluate"

)
def evaluate_status(

    business_id: int,

    db: Session = Depends(get_db)

):


    return evaluate_business_status(

        db=db,

        business_id=business_id

    )