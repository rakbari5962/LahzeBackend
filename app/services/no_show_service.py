from sqlalchemy.orm import Session
from datetime import datetime, timezone


from app.models.booking import Booking
from app.models.no_show_report import NoShowReport
from app.models.opportunity import Opportunity


from app.services.settlement_service import (
    settle_payment
)


from app.schemas.notification import NotificationCreate


from app.repositories.notification_repository import (
    create_notification
)



def report_no_show(
    db: Session,
    booking_id: int
):


    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()


    if not booking:
        return None



    # جلوگیری از ثبت مجدد No Show

    existing_report = db.query(NoShowReport).filter(
        NoShowReport.booking_id == booking_id
    ).first()


    if existing_report:
        return existing_report



    # فقط رزرو تایید شده می‌تواند No Show شود

    if booking.status != "CONFIRMED":
        return None



    report = NoShowReport(

        booking_id=booking.id,

        business_id=booking.business_id,

        status="PENDING"

    )


    db.add(report)



    booking.status = "NO_SHOW_REPORTED"



    db.commit()

    db.refresh(report)



    notification = NotificationCreate(

        user_id=booking.user_id,

        type="NO_SHOW_REPORTED",

        title="گزارش عدم حضور",

        message=(
            "کسب و کار اعلام کرده است که شما "
            "در زمان رزرو حضور نداشتید. "
            "در صورت اشتباه بودن، می‌توانید اعتراض ثبت کنید."
        )

    )


    create_notification(
        db,
        notification
    )


    return report





def dispute_no_show(
    db: Session,
    booking_id: int
):


    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()


    if not booking:
        return None



    report = db.query(NoShowReport).filter(
        NoShowReport.booking_id == booking_id
    ).first()



    if not report:
        return None



    # فقط No Show های در انتظار اعتراض قابل اعتراض هستند

    if report.status != "PENDING":
        return report



    # مشتری اعتراض کرده

    report.status = "CUSTOMER_DISPUTED"


    report.customer_response_at = datetime.now(
        timezone.utc
    )


    report.resolved_at = datetime.now(
        timezone.utc
    )



    # طبق Rule:
    # اعتراض مشتری = فرض بر انجام خدمت

    booking.status = "COMPLETED"


    booking.completed_at = datetime.now(
        timezone.utc
    )



    opportunity = db.query(Opportunity).filter(
        Opportunity.id == booking.opportunity_id
    ).first()



    if opportunity:

        settle_payment(
            db=db,
            booking_id=booking.id,
            business_id=booking.business_id,
            amount=opportunity.final_price
        )



    db.commit()


    db.refresh(report)


    return report