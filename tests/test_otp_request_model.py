from app.database.database import Base

from app.models.otp_request import OTPRequest


def test_otp_request_model():

    print(
        "OTP REQUEST MODEL TEST"
    )

    print(
        "====================="
    )


    tables = Base.metadata.tables.keys()


    print()

    print(
        "TABLES:"
    )

    print(
        tables
    )


    assert "otp_requests" in tables


    print()

    print(
        "OTP REQUEST MODEL PASSED ✅"
    )



if __name__ == "__main__":

    test_otp_request_model()