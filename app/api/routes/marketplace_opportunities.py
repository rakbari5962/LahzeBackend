from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db


from app.services.marketplace_opportunity_service import (
    get_marketplace_opportunities
)





router = APIRouter(

    prefix="/marketplace",

    tags=["Marketplace Opportunities"]

)







@router.get(

    "/opportunities"

)
def get_opportunities(

    city_id: int,

    category: str | None = None,

    db: Session = Depends(get_db)

):


    return get_marketplace_opportunities(

        db=db,

        city_id=city_id,

        category=category

    )