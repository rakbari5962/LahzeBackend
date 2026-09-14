from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.review_request import ReviewRequest
from app.schemas.notification import NotificationCreate
from app.repositories.notification_repository import create_notification



def create_review_request(
    db: Session,
    booking
):

    existing_request = db.query(ReviewRequest).filter(
        ReviewRequest.booking_id == booking.id
    ).first()


    if existing_request:
        return existing_request



    review_request = ReviewRequest(

        booking_id=booking.id,

        user_id=booking.user_id,

        business_id=booking.business_id,

        status="PENDING"

    )


    db.add(review_request)

    db.commit()

    db.refresh(review_request)



    # ساخت Notification برای مشتری
    notification = NotificationCreate(

        user_id=booking.user_id,

        type="REVIEW_REQUEST",

        title="تجربه خود را ثبت کنید",

        message="خدمت شما انجام شد. نظر خود را درباره تجربه‌تان ثبت کنید."

    )


    create_notification(

        db,

        notification

    )


    # تغییر وضعیت ReviewRequest بعد از ارسال
    review_request.status = "SENT"

    review_request.sent_at = datetime.now(
        timezone.utc
    )


    db.commit()

    db.refresh(review_request)



    return review_request





def get_user_review_requests(
    db: Session,
    user_id: int
):

    return db.query(ReviewRequest).filter(
        ReviewRequest.user_id == user_id
    ).all()





def complete_review_request(
    db: Session,
    review_request_id: int
):

    request = db.query(ReviewRequest).filter(
        ReviewRequest.id == review_request_id
    ).first()


    if not request:
        return None


    request.status = "COMPLETED"

    request.completed_at = datetime.now(
        timezone.utc
    )


    db.commit()

    db.refresh(request)


    return request