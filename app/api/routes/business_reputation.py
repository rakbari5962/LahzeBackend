from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.review_ai_analysis import (
    ReviewAIAnalysisResponse
)

from app.services.business_reputation_service import (
    get_business_reputation
)



router = APIRouter(
    prefix="/businesses",
    tags=["Business Reputation"]
)



@router.get(
    "/{business_id}/review-summary",
    response_model=ReviewAIAnalysisResponse
)
def business_review_summary(
    business_id: int,
    db: Session = Depends(get_db)
):

    result = get_business_reputation(
        db=db,
        business_id=business_id
    )


    if not result:

        raise HTTPException(
            status_code=404,
            detail="Review analysis not found"
        )


    return result