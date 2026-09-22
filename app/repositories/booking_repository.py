from sqlalchemy.orm import joinedload
from app.repositories.business_priority_access_repository import (
    create_priority_access,
    has_first_customer_access
)

from app.services.commission_service import (
    create_booking_commissions
)

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.booking import Booking
from app.models.opportunity import Opportunity
from app.models.business import Business
from app.models.user import User
from app.models.wallet_hold import WalletHold

from app.schemas.booking import (
    BookingCreate
)
from app.schemas.notification import NotificationCreate

from app.repositories.notification_repository import create_notification
from app.repositories.review_request_repository import create_review_request

from app.services.sms_service import (
    send_booking_notification,
    send_booking_confirmation_notification
)

from app.services.wallet_hold_service import (
    create_booking_hold,
    capture_booking_hold,
    release_booking_hold
)

from app.services.payment_service import (
    create_payment
)

from app.services.cancellation_service import (
    cancel_confirmed_booking
)

from app.services.settlement_service import (
    settle_payment
)



def create_booking(
    db: Session,
    booking: BookingCreate,
    user_id: int
):

    print(
        "CREATE BOOKING START",
        user_id,
        booking.opportunity_id
    )

    opportunity = db.query(Opportunity).filter(
        Opportunity.id == booking.opportunity_id
    ).first()


    if not opportunity:
        return None


    if opportunity.status != "ACTIVE":

        raise HTTPException(
            status_code=400,
            detail="Opportunity is not available"
        )


    if opportunity.reserved_count >= opportunity.capacity:

        opportunity.status = "FULL"

        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Opportunity capacity is full"
        )



    db_booking = Booking(
        user_id=user_id,
        business_id=opportunity.business_id,
        opportunity_id=booking.opportunity_id,
        status="PENDING_CONFIRMATION"
    )


    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)



    # بلوکه کردن مبلغ در کیف پول مشتری

    print(
        "BEFORE HOLD",
        user_id,
        opportunity.final_price
    )

    hold = create_booking_hold(
        db=db,
        user_id=user_id,
        booking_id=db_booking.id,
        amount=opportunity.final_price
    )

    print("HOLD RESULT", hold)


    if not hold:

        db.delete(db_booking)
        db.commit()

        raise HTTPException(
             status_code=400,
             detail="Insufficient wallet balance"
         )
    opportunity.reserved_count += 1


    if opportunity.reserved_count >= opportunity.capacity:

        opportunity.status = "FULL"


    db.commit()


    # ایجاد کمیسیون‌های معرفی به صورت PENDING
    # در این مرحله هیچ مبلغی وارد Wallet نمی‌شود

    commission_events = create_booking_commissions(
        db=db,
        business_id=opportunity.business_id,
        booking_id=db_booking.id,
        amount=opportunity.final_price
    )

    print(
        "PENDING COMMISSION EVENTS:",
        [
            {
                "id": event.id,
                "user_id": event.user_id,
                "amount": event.amount,
                "status": event.status
            }
            for event in commission_events
        ]
    )




    business = db.query(Business).filter(
        Business.id == opportunity.business_id
    ).first()



    if business:


        notification = NotificationCreate(
            user_id=business.owner_user_id,
            type="NEW_BOOKING",
            title="رزرو جدید",
            message="یک مشتری درخواست رزرو جدید ثبت کرده است."
        )


        create_notification(
            db,
            notification
        )



        owner = db.query(User).filter(
            User.id == business.owner_user_id
        ).first()



        if owner:

            try:

                send_booking_notification(
                    mobile=owner.phone_number,
                    business_name=business.name,
                    booking_id=db_booking.id
                )


            except Exception as e:

                print(
                    "BOOKING SMS ERROR:",
                    repr(e)
                )



    return db_booking





def get_booking(
    db: Session,
    booking_id: int
):

    booking = db.query(Booking)\
        .options(
            joinedload(Booking.business),
            joinedload(Booking.opportunity)
        )\
        .filter(
            Booking.id == booking_id
        )\
        .first()


    if not booking:
        return None



    wallet_hold = db.query(WalletHold).filter(
        WalletHold.booking_id == booking_id
    ).first()



    return {
        "id": booking.id,

        "user_id": booking.user_id,

        "business_id": booking.business_id,

        "opportunity_id": booking.opportunity_id,

        "status": booking.status,

        "created_at": booking.created_at,

        "confirmed_at": booking.confirmed_at,

        "completed_at": booking.completed_at,

        "cancelled_at": booking.cancelled_at,


        "business": booking.business,

        "opportunity": booking.opportunity,


        "wallet_hold": wallet_hold
    }





def get_user_bookings(
    db: Session,
    user_id: int
):

    bookings = db.query(Booking).filter(
        Booking.user_id == user_id
    ).order_by(
        Booking.created_at.desc()
    ).all()


    result = []


    for booking in bookings:


        business = db.query(Business).filter(
            Business.id == booking.business_id
        ).first()


        opportunity = db.query(Opportunity).filter(
            Opportunity.id == booking.opportunity_id
        ).first()


        result.append(
            {
                "id": booking.id,

                "user_id": booking.user_id,

                "business_id": booking.business_id,

                "opportunity_id": booking.opportunity_id,

                "status": booking.status,

                "created_at": booking.created_at,

                "confirmed_at": booking.confirmed_at,

                "completed_at": booking.completed_at,

                "cancelled_at": booking.cancelled_at,


                "business": business,

                "opportunity": opportunity
            }
        )


    return result





def confirm_booking(
    db: Session,
    booking_id: int
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()


    if not booking:
        return None


    # Idempotency:
    # اگر قبلاً تایید شده، همان Booking را برگردان
    # و Payment دوباره ساخته نشود

    if booking.status == "CONFIRMED":
        return booking


    if booking.status != "PENDING_CONFIRMATION":
        raise HTTPException(
             status_code=400,
             detail="Booking cannot be confirmed"
         )



    opportunity = db.query(Opportunity).filter(
        Opportunity.id == booking.opportunity_id
    ).first()



    if not opportunity:
        return None



    try:


        # تبدیل مبلغ بلوکه شده به پرداخت قطعی

        hold = capture_booking_hold(
            db=db,
            booking_id=booking.id
        )


        if not hold:

            print(
                "HOLD NOT FOUND:",
                booking.id
            )

            return None




        # انتقال پول به Escrow

        payment = create_payment(
            db=db,
            user_id=booking.user_id,
            amount=opportunity.final_price,
            booking_id=booking.id
        )


        if not payment:

            print(
                "PAYMENT FAILED:",
                booking.id
            )

            return None




        booking.status = "CONFIRMED"

        booking.confirmed_at = datetime.now(
            timezone.utc
        )


        # ثبت First Customer Priority Access

        if not has_first_customer_access(
            db=db,
            business_id=booking.business_id
        ):

            create_priority_access(
                db=db,
                business_id=booking.business_id,
                user_id=booking.user_id,
                access_type="FIRST_CUSTOMER",
                source_id=booking.id
            )


        db.commit()

        db.refresh(booking)

    



        notification = NotificationCreate(
            user_id=booking.user_id,
            type="BOOKING_CONFIRMED",
            title="رزرو تایید شد",
            message="رزرو شما توسط کسب و کار تایید شد."
        )


        create_notification(
            db,
            notification
        )





        customer = db.query(User).filter(
            User.id == booking.user_id
        ).first()



        business = db.query(Business).filter(
            Business.id == booking.business_id
        ).first()



        if customer and business:

            try:

                send_booking_confirmation_notification(
                    mobile=customer.phone_number,
                    business_name=business.name,
                    booking_id=booking.id
                )


            except Exception as e:

                print(
                    "BOOKING CONFIRM SMS ERROR:",
                    repr(e)
                )




        print(
            "BOOKING CONFIRMED:",
            booking.id
        )


        return booking




    except Exception as e:

        db.rollback()

        print(
            "CONFIRM BOOKING ERROR:",
            repr(e)
        )

        raise





def cancel_booking(
    db: Session,
    booking_id: int
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()


    if not booking:
        return None



    # قبل از تایید سالن:
    # Hold آزاد می‌شود
    # بدون جریمه

    if booking.status == "PENDING_CONFIRMATION":


        release_booking_hold(
            db,
            booking_id
        )


        opportunity = db.query(Opportunity).filter(
            Opportunity.id == booking.opportunity_id
        ).first()


        if opportunity:


            if opportunity.reserved_count > 0:

                opportunity.reserved_count -= 1



            if opportunity.reserved_count < opportunity.capacity:

                opportunity.status = "ACTIVE"



        booking.status = "CANCELLED"


        booking.cancelled_at = datetime.now(
            timezone.utc
        )


        db.commit()

        db.refresh(booking)


        return booking




    # بعد از تایید سالن:
    # لغو مستقیم ممنوع است
    #
    # مسیر صحیح:
    # cancel-preview
    #       ↓
    # cancel-confirm

    if booking.status == "CONFIRMED":

        raise HTTPException(
        status_code=400,
        detail="Confirmed booking must use cancel confirmation flow"
        )
        return None




    # COMPLETED یا CANCELLED
    # دوباره قابل لغو نیستند

    return None





def complete_booking(
    db: Session,
    booking_id: int
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()



    if not booking:
        return None



# Idempotency:
# اگر قبلاً کامل شده، دوباره Settlement اجرا نشود

    if booking.status == "COMPLETED":
        return booking


    if booking.status != "CONFIRMED":
        raise HTTPException(
            status_code=400,
            detail="Booking cannot be completed"
        )



    try:


        booking.status = "COMPLETED"


        booking.completed_at = datetime.now(
            timezone.utc
        )


        db.commit()
        db.refresh(booking)




        notification = NotificationCreate(
            user_id=booking.user_id,
            type="BOOKING_COMPLETED",
            title="خدمت انجام شد",
            message="خدمت شما با موفقیت انجام شد. اکنون می‌توانید تجربه خود را ثبت کنید."
        )


        create_notification(
            db,
            notification
        )




        create_review_request(
            db,
            booking
        )





        opportunity = db.query(Opportunity).filter(
            Opportunity.id == booking.opportunity_id
        ).first()



        if opportunity:


            settlement_result = settle_payment(
                db=db,
                booking_id=booking.id,
                business_id=booking.business_id,
                amount=opportunity.final_price
            )


            print(
                "SETTLEMENT RESULT:",
                settlement_result
            )



        return booking



    except Exception as e:


        db.rollback()


        print(
            "COMPLETE BOOKING ERROR:",
            repr(e)
        )


        raise