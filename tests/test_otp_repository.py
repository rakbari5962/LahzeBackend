from datetime import datetime, timedelta, timezone


from app.database.database import SessionLocal


from app.repositories.otp_repository import (

    create_otp_request,

    get_latest_otp,

    mark_otp_verified,

    invalidate_old_otps

)





def test_otp_repository():


    print(
        "OTP REPOSITORY TEST"
    )

    print(
        "=================="
    )


    db = SessionLocal()



    phone_number = "09990000099"



    # CREATE OTP


    otp = create_otp_request(

        db=db,

        phone_number=phone_number,

        code="123456",

        expires_at=datetime.now(timezone.utc) + timedelta(minutes=2)

    )



    print()

    print(
        "OTP CREATED:",
        otp.id
    )



    assert otp.phone_number == phone_number

    assert otp.code == "123456"





    # GET LATEST OTP


    latest = get_latest_otp(

        db=db,

        phone_number=phone_number

    )



    print()

    print(
        "LATEST OTP:",
        latest.code
    )



    assert latest.code == "123456"





    # VERIFY OTP


    verified = mark_otp_verified(

        db=db,

        otp_request=latest

    )



    print()

    print(
        "OTP VERIFIED:",
        verified.is_verified
    )



    assert verified.is_verified is True





    # CREATE ANOTHER OTP


    second = create_otp_request(

        db=db,

        phone_number=phone_number,

        code="654321",

        expires_at=datetime.now(timezone.utc) + timedelta(minutes=2)

    )



    print()

    print(
        "SECOND OTP:",
        second.code
    )





    # INVALIDATE OLD OTPs


    invalidate_old_otps(

        db=db,

        phone_number=phone_number

    )



    latest_after = get_latest_otp(

        db=db,

        phone_number=phone_number

    )



    print()

    print(
        "LATEST AFTER INVALIDATE:",
        latest_after.code
    )



    db.close()



    print()

    print(
        "OTP REPOSITORY PASSED ✅"
    )





if __name__ == "__main__":

    test_otp_repository()