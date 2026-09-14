from datetime import datetime, timedelta, timezone


from app.database.database import SessionLocal

from app.models.otp_request import OTPRequest

from app.services.otp_policy import can_request_otp





def test_otp_rate_limit():


    print(
        "OTP RATE LIMIT TEST"
    )

    print(
        "=================="
    )



    db = SessionLocal()



    phone_number = "09129367314"



    now = datetime.now(timezone.utc)



    times = [

        14,

        10,

        7,

        5,

        2

    ]



    for index, minutes in enumerate(times):


        otp = OTPRequest(

            phone_number=phone_number,

            code=str(100000 + index),

            expires_at=(

                now

                +

                timedelta(minutes=2)

            ),

            created_at=(

                now

                -

                timedelta(minutes=minutes)

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


    assert result["reason"] == "OTP_RATE_LIMIT"





    print()

    print(
        "OTP RATE LIMIT PASSED ✅"
    )



    db.close()





if __name__ == "__main__":

    test_otp_rate_limit()