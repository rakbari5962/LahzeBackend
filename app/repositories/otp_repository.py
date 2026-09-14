from sqlalchemy.orm import Session

from sqlalchemy import desc

from datetime import datetime


from app.models.otp_request import OTPRequest





def create_otp_request(
    db: Session,
    phone_number: str,
    code: str,
    expires_at: datetime
):


    otp_request = OTPRequest(

        phone_number=phone_number,

        code=code,

        expires_at=expires_at,

        is_verified=False

    )


    db.add(

        otp_request

    )


    db.commit()


    db.refresh(

        otp_request

    )


    return otp_request





def get_latest_otp(
    db: Session,
    phone_number: str
):


    return (

        db.query(

            OTPRequest

        )

        .filter(

            OTPRequest.phone_number == phone_number

        )

        .order_by(

            desc(

                OTPRequest.created_at

            )

        )

        .first()

    )





def mark_otp_verified(
    db: Session,
    otp_request: OTPRequest
):


    otp_request.is_verified = True

    otp_request.verified_at = datetime.utcnow()


    db.commit()


    db.refresh(

        otp_request

    )


    return otp_request





def invalidate_old_otps(
    db: Session,
    phone_number: str
):


    db.query(

        OTPRequest

    ).filter(

        OTPRequest.phone_number == phone_number,

        OTPRequest.is_verified == False

    ).update(

        {

            "is_verified": True

        }

    )


    db.commit()