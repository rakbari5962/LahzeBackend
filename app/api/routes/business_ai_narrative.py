from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.business_ai_narrative import (
    BusinessAINarrativeResponse
)


from app.services.business_ai_narrative_query_service import (
    get_business_ai_summary
)



router = APIRouter(

    prefix="/businesses",

    tags=["Business AI Narrative"]

)




@router.get(

    "/{business_id}/ai-summary",

    response_model=BusinessAINarrativeResponse

)
def business_ai_summary(

    business_id: int,

    db: Session = Depends(get_db)

):


    result = get_business_ai_summary(

        db=db,

        business_id=business_id

    )


    if not result:

        raise HTTPException(

            status_code=404,

            detail="AI summary not found"

        )


    return result