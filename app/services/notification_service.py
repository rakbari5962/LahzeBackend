from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User

from app.services.sms_service import send_booking_notification



def notify_new_booking(
    db: Session,
    business_owner_user_id: int,
    business_name: str,
    booking_id: int
):

    owner = (
        db.query(User)
        .filter(
            User.id == business_owner_user_id
        )
        .first()
    )


    if not owner:
        return None


    message = (
        f"رزرو جدیدی برای {business_name} "
        f"ثبت شده است. لطفاً وارد سامانه لحظه شوید."
    )


    notification = Notification(
        user_id=owner.id,
        type="NEW_BOOKING",
        title="رزرو جدید",
        message=message
    )


    db.add(notification)

    db.commit()

    db.refresh(notification)



    # ارسال SMS
    send_booking_notification(
        mobile=owner.phone_number,
        business_name=business_name,
        booking_id=booking_id
    )


    return notification