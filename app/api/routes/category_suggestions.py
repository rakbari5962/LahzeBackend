from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.category_suggestion import (
    CategorySuggestionCreate,
    CategorySuggestionResponse
)


from app.services.category_suggestion_service import (
    create_suggestion,
    get_suggestion,
    approve_suggestion,
    reject_suggestion
)



router = APIRouter(

    prefix="/category-suggestions",

    tags=["Category Suggestions"]

)



@router.post(
    "/",
    response_model=CategorySuggestionResponse
)
def create_new_suggestion(

    data: CategorySuggestionCreate,

    db: Session = Depends(get_db)

):

    return create_suggestion(

        db=db,

        business_id=data.business_id,

        suggested_category_id=data.suggested_category_id,

        confidence=data.confidence,

        reason=data.reason

    )





@router.get(
    "/{suggestion_id}",
    response_model=CategorySuggestionResponse
)
def read_suggestion(

    suggestion_id: int,

    db: Session = Depends(get_db)

):

    return get_suggestion(

        db,

        suggestion_id

    )





@router.patch(
    "/{suggestion_id}/approve",
    response_model=CategorySuggestionResponse
)
def approve_existing_suggestion(

    suggestion_id: int,

    db: Session = Depends(get_db)

):

    return approve_suggestion(

        db,

        suggestion_id

    )





@router.patch(
    "/{suggestion_id}/reject",
    response_model=CategorySuggestionResponse
)
def reject_existing_suggestion(

    suggestion_id: int,

    db: Session = Depends(get_db)

):

    return reject_suggestion(

        db,

        suggestion_id

    )