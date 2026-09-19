from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.business_attribute_service import (
    get_business_attribute_summary
)


router = APIRouter(
    prefix="/businesses",
    tags=["Business Attributes"]
)


@router.get(
    "/{business_id}/attributes"
)
def get_business_attributes(
    business_id: int,
    db: Session = Depends(get_db)
):

    return get_business_attribute_summary(
        db=db,
        business_id=business_id
    )