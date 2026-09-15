from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.models.opportunity import Opportunity

from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingCancelPreviewResponse
)

from app.repositories.booking_repository import (
    create_booking,
    get_booking,
    get_user_bookings,
    confirm_booking,
    cancel_booking,
    complete_booking
)

from app.services.cancellation_service import (
    preview_cancel_confirmed_booking,
    cancel_confirmed_booking
)



router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)





@router.post(
    "/",
    response_model=BookingResponse
)
def create_new_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    print("BOOKING ROUTE HIT")

    return create_booking(
        db,
        booking
    )





@router.get(
    "/{booking_id}",
    response_model=BookingResponse
)
def read_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    return get_booking(
        db,
        booking_id
    )





@router.get(
    "/user/{user_id}",
    response_model=list[BookingResponse]
)
def read_user_bookings(
    user_id: int,
    db: Session = Depends(get_db)
):

    return get_user_bookings(
        db,
        user_id
    )





# تایید رزرو توسط کسب و کار

@router.patch(
    "/{booking_id}/confirm",
    response_model=BookingResponse
)
def confirm_booking_request(
    booking_id: int,
    db: Session = Depends(get_db)
):

    return confirm_booking(
        db,
        booking_id
    )





# نمایش جریمه قبل از لغو

@router.post(
    "/{booking_id}/cancel-preview",
    response_model=BookingCancelPreviewResponse
)
def cancel_preview_request(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = get_booking(
        db,
        booking_id
    )


    if not booking:
        return None



    opportunity = db.query(Opportunity).filter(
        Opportunity.id == booking.opportunity_id
    ).first()



    if not opportunity:
        return None



    return preview_cancel_confirmed_booking(
        db=db,
        booking_id=booking_id,
        amount=opportunity.final_price
    )





# تایید نهایی لغو توسط مشتری

@router.patch(
    "/{booking_id}/cancel-confirm",
    response_model=BookingResponse
)
def cancel_confirm_request(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = get_booking(
        db,
        booking_id
    )


    if not booking:
        return None



    opportunity = db.query(Opportunity).filter(
        Opportunity.id == booking.opportunity_id
    ).first()



    if not opportunity:
        return None



    result = cancel_confirmed_booking(
        db=db,
        booking_id=booking_id,
        amount=opportunity.final_price
    )


    if not result:
        return None


    return result





# لغو رزرو
# فعلاً نگه داشته شده؛ بعد از تست cancel-confirm محدود می‌شود

@router.patch(
    "/{booking_id}/cancel",
    response_model=BookingResponse
)
def cancel_booking_request(
    booking_id: int,
    db: Session = Depends(get_db)
):

    return cancel_booking(
        db,
        booking_id
    )





# پایان خدمت

@router.patch(
    "/{booking_id}/complete",
    response_model=BookingResponse
)
def complete_booking_request(
    booking_id: int,
    db: Session = Depends(get_db)
):

    return complete_booking(
        db,
        booking_id
    )