import random

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session


from app.models.user import User


from app.repositories.otp_repository import (
    create_otp_request,
    get_latest_otp,
    mark_otp_verified,
    invalidate_old_otps
)


from app.repositories.invitation_repository import (
    get_invitation,
    accept_invitation
)


from app.services.sms_service import send_verification_code


from app.services.otp_policy import can_request_otp


from app.services.session_service import create_login_session


from app.core.errors.exceptions import LahzeException

from app.core.errors.error_codes import ErrorCodes





OTP_EXPIRE_MINUTES = 10





def generate_otp():

    return str(

        random.randint(

            100000,

            999999

        )

    )









def request_otp(

    db: Session,

    phone_number: str

):


    policy = can_request_otp(

        db=db,

        phone_number=phone_number

    )



    if not policy["allowed"]:


        if policy["reason"] == "OTP_COOLDOWN":


            raise LahzeException(

                error_code=ErrorCodes.OTP_COOLDOWN,

                message="Please wait before requesting another OTP",

                context=policy

            )



        if policy["reason"] == "OTP_RATE_LIMIT":


            raise LahzeException(

                error_code=ErrorCodes.OTP_RATE_LIMIT,

                message="Too many OTP requests",

                context=policy

            )



    invalidate_old_otps(

        db,

        phone_number

    )



    code = generate_otp()



    expires_at = (

        datetime.now(timezone.utc)

        +

        timedelta(

            minutes=OTP_EXPIRE_MINUTES

        )

    )



    otp = create_otp_request(

        db=db,

        phone_number=phone_number,

        code=code,

        expires_at=expires_at

    )



    send_verification_code(

        mobile=phone_number,

        code=code

    )



    return otp









def verify_otp(

    db: Session,

    phone_number: str,

    code: str,

    invitation_id: int | None = None

):


    otp = get_latest_otp(

        db,

        phone_number

    )





    if not otp:


        raise LahzeException(

            error_code=ErrorCodes.OTP_NOT_FOUND,

            message="OTP not found"

        )





    if otp.is_verified:


        raise LahzeException(

            error_code=ErrorCodes.OTP_ALREADY_USED,

            message="OTP already used"

        )





    if otp.expires_at < datetime.now(timezone.utc):


        raise LahzeException(

            error_code=ErrorCodes.OTP_EXPIRED,

            message="OTP expired"

        )





    if otp.code != code:


        raise LahzeException(

            error_code=ErrorCodes.OTP_INVALID,

            message="Invalid OTP"

        )





    mark_otp_verified(

        db,

        otp

    )





    user = (

        db.query(User)

        .filter(

            User.phone_number == phone_number

        )

        .first()

    )





    if not user:


        user = User(

            phone_number=phone_number,

            role="CUSTOMER",

            profile_completed=False

        )


        db.add(user)

        db.commit()

        db.refresh(user)





    # Accept Invitation if user entered through invitation link

    if invitation_id:


        invitation = get_invitation(

            db=db,

            invitation_id=invitation_id

        )


        if invitation and invitation.status == "PENDING":


            accept_invitation(

                db=db,

                invitation=invitation,

                user_id=user.id,

                user_phone=user.phone_number

            )





    # تعیین نوع Session بر اساس تکمیل Profile

    is_temporary = not user.profile_completed





    # ساخت Session Login

    session = create_login_session(

        db=db,

        user_id=user.id,

        is_temporary=is_temporary

    )





    return {

        "user": user,

        "session": session,

        "requires_city_selection": not user.profile_completed

    }