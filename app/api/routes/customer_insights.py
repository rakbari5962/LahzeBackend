from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.customer_insight_service import (
    get_customer_insights
)


router = APIRouter(
    prefix="/businesses",
    tags=["Customer Insights"]
)


@router.get(
    "/{business_id}/customer-insights"
)
def customer_insights(
    business_id: int,
    db: Session = Depends(get_db)
):

    return get_customer_insights(
        db=db,
        business_id=business_id
    )