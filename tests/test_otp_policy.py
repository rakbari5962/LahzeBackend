from datetime import datetime, timedelta, timezone

from app.database.database import SessionLocal

from app.models.otp_request import OTPRequest

from app.services.otp_policy import can_request_otp





def test_otp_policy():

    print(
        "OTP POLICY TEST"
    )

    print(
        "==============="
    )


    db = SessionLocal()


    phone_number = "09129367314"



    # FIRST REQUEST

    otp = OTPRequest(

        phone_number=phone_number,

        code="123456",

        expires_at=(

            datetime.now(timezone.utc)

            +

            timedelta(minutes=2)

        )

    )


    db.add(otp)

    db.commit()



    result = can_request_otp(

        db=db,

        phone_number=phone_number

    )


    print()

    print(
        "POLICY RESULT:"
    )

    print(
        result
    )


    assert result["allowed"] is False

    assert result["reason"] == "OTP_COOLDOWN"



    print()

    print(
        "OTP POLICY PASSED ✅"
    )


    db.close()





if __name__ == "__main__":

    test_otp_policy()