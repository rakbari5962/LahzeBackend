from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.otp_request import OTPRequest





RESEND_COOLDOWN_SECONDS = 60

MAX_REQUESTS = 5

RATE_LIMIT_MINUTES = 15





def can_request_otp(

    db: Session,

    phone_number: str

):


    now = datetime.now(timezone.utc)



    # آخرین OTP

    latest_otp = (

        db.query(OTPRequest)

        .filter(

            OTPRequest.phone_number == phone_number

        )

        .order_by(

            OTPRequest.id.desc()

        )

        .first()

    )



    if latest_otp:


        if latest_otp.created_at:


            elapsed = (

                now - latest_otp.created_at

            ).total_seconds()



            if elapsed < RESEND_COOLDOWN_SECONDS:


                return {

                    "allowed": False,

                    "reason": "OTP_COOLDOWN",

                    "retry_after":

                        RESEND_COOLDOWN_SECONDS - int(elapsed)

                }



    # تعداد درخواست‌ها در بازه زمانی

    limit_time = (

        now -

        timedelta(

            minutes=RATE_LIMIT_MINUTES

        )

    )



    requests_count = (

        db.query(OTPRequest)

        .filter(

            OTPRequest.phone_number == phone_number,

            OTPRequest.created_at >= limit_time

        )

        .count()

    )



    if requests_count >= MAX_REQUESTS:


        return {

            "allowed": False,

            "reason": "OTP_RATE_LIMIT"

        }



    return {

        "allowed": True

    }