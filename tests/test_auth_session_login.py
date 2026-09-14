from app.database.database import SessionLocal

from app.services.auth_service import verify_otp

from app.models.user import User

from app.models.session import Session as UserSession

from app.models.otp_request import OTPRequest





def test_auth_session_login():

    print(
        "AUTH SESSION LOGIN TEST"
    )

    print(
        "======================"
    )


    db = SessionLocal()


    phone_number = "09129367314"



    # آخرین OTP تایید نشده را پیدا می‌کنیم

    otp = (

        db.query(OTPRequest)

        .filter(

            OTPRequest.phone_number == phone_number,

            OTPRequest.is_verified == False

        )

        .order_by(

            OTPRequest.id.desc()

        )

        .first()

    )


    assert otp is not None



    result = verify_otp(

        db=db,

        phone_number=phone_number,

        code=otp.code

    )


    user = result["user"]

    session = result["session"]



    print()

    print(
        "USER:"
    )

    print(
        user.id,
        user.phone_number
    )


    print()

    print(
        "SESSION:"
    )

    print(
        session.id
    )

    print(
        session.token
    )


    print()

    print(
        "PROFILE:"
    )

    print(
        user.profile_completed
    )


    print()

    print(
        "TEMPORARY:"
    )

    print(
        session.is_temporary
    )



    assert user.phone_number == phone_number

    assert session.user_id == user.id

    assert session.is_active is True


    # Temporary Session Flow

    assert user.profile_completed is False

    assert session.is_temporary is True

    assert result["requires_city_selection"] is True



    db.close()


    print()

    print(
        "AUTH SESSION LOGIN PASSED ✅"
    )





if __name__ == "__main__":

    test_auth_session_login()