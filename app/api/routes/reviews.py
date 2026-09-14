from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.review import (
    ReviewCreate,
    ReviewResponse
)

from app.repositories.review_repository import (
    create_review,
    get_business_reviews,
    get_user_reviews
)


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)



@router.post(
    "/",
    response_model=ReviewResponse
)
def create_new_review(
    review: ReviewCreate,
    db: Session = Depends(get_db)
):

    result = create_review(
        db,
        review
    )


    if isinstance(result, dict) and "error" in result:

        errors = {

            "BOOKING_NOT_FOUND":
                "Booking not found",

            "BOOKING_NOT_COMPLETED":
                "Review is only allowed after completed booking",

            "ALREADY_REVIEWED":
                "You already reviewed this booking"
        }


        raise HTTPException(
            status_code=400,
            detail=errors[result["error"]]
        )


    return result





@router.get(
    "/business/{business_id}",
    response_model=list[ReviewResponse]
)
def read_business_reviews(
    business_id: int,
    db: Session = Depends(get_db)
):

    return get_business_reviews(
        db,
        business_id
    )





@router.get(
    "/user/{user_id}",
    response_model=list[ReviewResponse]
)
def read_user_reviews(
    user_id: int,
    db: Session = Depends(get_db)
):

    return get_user_reviews(
        db,
        user_id
    )