from fastapi.testclient import TestClient

from unittest.mock import patch, Mock


from app.main import app

from app.database.database import SessionLocal

from app.models.otp_request import OTPRequest

import os

from app.main import app

client = TestClient(app)





def test_auth_api():


    print(
        "AUTH API TEST"
    )

    print(
        "=============="
    )



    phone_number = "09129367314"
    
    os.environ["SMS_IR_API_KEY"] = "TEST_KEY"

    os.environ["SMS_IR_TEMPLATE_ID"] = "123456"



    mock_response = Mock()

    mock_response.json.return_value = {

        "status": 1,

        "message": "موفق"

    }

    mock_response.raise_for_status.return_value = None





    with patch(

        "app.services.sms_service.requests.post",

        return_value=mock_response

    ):



        # REQUEST OTP


        response = client.post(

            "/auth/request-otp",

            params={

                "phone_number": phone_number

            }

        )



        print()

        print(
            "REQUEST OTP:"
        )

        print(
            response.status_code
        )

        print(
            response.json()
        )



        assert response.status_code == 200





    # READ OTP FROM DATABASE

    db = SessionLocal()



    otp = (

        db.query(OTPRequest)

        .filter(

            OTPRequest.phone_number == phone_number

        )

        .order_by(

            OTPRequest.id.desc()

        )

        .first()

    )



    print()

    print(
        "OTP FROM DATABASE:",
        otp.code
    )





    # VERIFY OTP


    response = client.post(

        "/auth/verify-otp",

        params={

            "phone_number": phone_number,

            "code": otp.code

        }

    )



    print()

    print(
        "VERIFY OTP:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 200



    data = response.json()



    assert data["success"] is True

    assert data["phone_number"] == phone_number



    db.close()



    print()

    print(
        "AUTH API PASSED ✅"
    )





if __name__ == "__main__":

    test_auth_api()