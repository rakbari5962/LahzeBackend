from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate



def create_notification(
    db: Session,
    notification: NotificationCreate
):

    db_notification = Notification(
        user_id=notification.user_id,
        type=notification.type,
        title=notification.title,
        message=notification.message
    )


    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification



def get_user_notifications(
    db: Session,
    user_id: int
):

    return db.query(Notification).filter(
        Notification.user_id == user_id
    ).all()



def mark_as_read(
    db: Session,
    notification_id: int
):

    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()


    if not notification:
        return None


    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification