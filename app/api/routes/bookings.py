from app.schemas.no_show import (
    NoShowReportResponse
)

from app.services.no_show_service import (
    report_no_show,
    dispute_no_show
)


from fastapi import APIRouter, Depends, HTTPException

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

from app.services.session_service import (
    get_login_session
)

from app.repositories.user_repository import (
    get_user
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post(
    "/{booking_id}/no-show-dispute",
    response_model=NoShowReportResponse
)
def dispute_no_show_request(
    booking_id: int,
    db: Session = Depends(get_db)
):

    return dispute_no_show(
        db,
        booking_id
    )







@router.post(
    "/",
    response_model=BookingResponse
)
def create_new_booking(
    booking: BookingCreate,
    token: str,
    db: Session = Depends(get_db)
):

    print("BOOKING ROUTE HIT")


    session = get_login_session(
        db=db,
        token=token
    )


    if not session:

        raise HTTPException(
            status_code=401,
            detail="LOGIN_REQUIRED"
        )


    user = get_user(
        db,
        session.user_id
    )


    if not user:

        raise HTTPException(
            status_code=404,
            detail="USER_NOT_FOUND"
        )


    if not user.profile_completed:

        raise HTTPException(
            status_code=403,
            detail="PROFILE_COMPLETION_REQUIRED"
        )


    return create_booking(
            db,
            booking,
            session.user_id
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

# گزارش عدم حضور مشتری توسط کسب و کار

@router.post(
    "/{booking_id}/no-show",
    response_model=NoShowReportResponse
)
def report_no_show_request(
    booking_id: int,
    db: Session = Depends(get_db)
):

    return report_no_show(
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