from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.notification import (
    NotificationResponse
)

from app.repositories.notification_repository import (
    get_user_notifications,
    mark_as_read
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)



@router.get(
    "/user/{user_id}",
    response_model=list[NotificationResponse]
)
def read_user_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):

    return get_user_notifications(
        db,
        user_id
    )



@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):

    return mark_as_read(
        db,
        notification_id
    )