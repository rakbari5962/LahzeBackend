from fastapi.testclient import TestClient

from unittest.mock import patch, Mock

import os

from app.main import app


client = TestClient(app)





def test_auth_error_api():


    print(
        "AUTH ERROR API TEST"
    )

    print(
        "=================="
    )



    phone_number = "09129367314"



    # ENV FOR SMS SERVICE

    os.environ["SMS_IR_API_KEY"] = "TEST_API_KEY"

    os.environ["SMS_IR_TEMPLATE_ID"] = "123456"





    # MOCK SMS RESPONSE


    mock_response = Mock()


    mock_response.json.return_value = {

        "status": 1,

        "message": "موفق",

        "data": {

            "messageId": 12345,

            "cost": 1

        }

    }


    mock_response.raise_for_status.return_value = None





    with patch(

        "app.services.sms_service.requests.post",

        return_value=mock_response

    ):



        # REQUEST OTP FIRST


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





    # INVALID OTP TEST


    response = client.post(

        "/auth/verify-otp",

        params={

            "phone_number": phone_number,

            "code": "111111"

        }

    )



    print()

    print(
        "INVALID OTP RESPONSE:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )





    assert response.status_code == 400



    data = response.json()



    assert data["success"] is False



    assert data["error"]["code"] == 202





    print()

    print(
        "AUTH ERROR API PASSED ✅"
    )





if __name__ == "__main__":

    test_auth_error_api()