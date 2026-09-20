from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.database import SessionLocal

from app.schemas.review import (
    ReviewCreate,
    ReviewResponse
)

from app.repositories.review_repository import (
    create_review,
    get_business_reviews,
    get_user_reviews
)

from app.services.review_ai_analysis_service import (
    analyze_business_reviews
)

from app.services.business_ai_narrative_service import (
    generate_business_narrative
)



router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)



def run_review_ai_pipeline(
    business_id: int
):

    db = SessionLocal()

    try:

        analyze_business_reviews(
            db=db,
            business_id=business_id
        )


        generate_business_narrative(
            db=db,
            business_id=business_id
        )


    except Exception as e:

        print(
            "BACKGROUND AI PIPELINE ERROR:",
            str(e)
        )


    finally:

        db.close()





@router.post(
    "/",
    response_model=ReviewResponse
)
def create_new_review(
    review: ReviewCreate,
    background_tasks: BackgroundTasks,
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


    business_id = result.business_id


    background_tasks.add_task(
        run_review_ai_pipeline,
        business_id
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