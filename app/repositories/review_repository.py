from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.booking import Booking
from app.models.review_request import ReviewRequest

from app.schemas.review import ReviewCreate
from app.repositories.review_request_repository import complete_review_request
from app.repositories.reward_event_repository import create_reward_event



def create_review(
    db: Session,
    review: ReviewCreate
):

    booking = db.query(Booking).filter(
        Booking.id == review.booking_id
    ).first()


    if not booking:
        return {
            "error": "BOOKING_NOT_FOUND"
        }


    if booking.status != "COMPLETED":
        return {
            "error": "BOOKING_NOT_COMPLETED"
        }


    existing_review = db.query(Review).filter(
        Review.booking_id == review.booking_id
    ).first()


    if existing_review:
        return {
            "error": "ALREADY_REVIEWED"
        }


    db_review = Review(
        booking_id=booking.id,
        user_id=booking.user_id,
        business_id=booking.business_id,
        rating=review.rating,
        comment=review.comment
    )


    db.add(db_review)
    db.commit()
    db.refresh(db_review)



    # پیدا کردن ReviewRequest مربوط به این Booking
    review_request = db.query(ReviewRequest).filter(
        ReviewRequest.booking_id == booking.id
    ).first()



    if review_request:

        complete_review_request(
            db,
            review_request.id
        )


        # ایجاد Reward Event
        create_reward_event(
            db,
            user_id=booking.user_id,
            booking_id=booking.id,
            review_id=db_review.id,
            reward_type="REVIEW_REWARD",
            amount=1
        )


    return db_review





def get_business_reviews(
    db: Session,
    business_id: int
):

    return db.query(Review).filter(
        Review.business_id == business_id
    ).all()





def get_user_reviews(
    db: Session,
    user_id: int
):

    return db.query(Review).filter(
        Review.user_id == user_id
    ).all()