from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.services.opportunity_expiration_service import (
    expire_old_opportunities
)





router = APIRouter(

    prefix="/opportunities",

    tags=["Opportunity Expiration"]

)





@router.post(
    "/expire"
)
def expire_opportunities(

    db: Session = Depends(get_db)

):

    return expire_old_opportunities(

        db=db

    )