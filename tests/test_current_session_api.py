from fastapi.testclient import TestClient

from unittest.mock import patch, Mock

from app.main import app


client = TestClient(app)



def test_current_session_api():

    print(
        "CURRENT SESSION API TEST"
    )

    print(
        "======================="
    )


    phone_number = "09129367314"



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


        response = client.post(

            "/auth/request-otp",

            params={

                "phone_number": phone_number

            }

        )


        assert response.status_code == 200



    # گرفتن OTP از دیتابیس

    from app.database.database import SessionLocal

    from app.models.otp_request import OTPRequest


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


    code = otp.code


    db.close()



    login_response = client.post(

        "/auth/verify-otp",

        params={

            "phone_number": phone_number,

            "code": code

        }

    )


    print()

    print(
        "LOGIN:"
    )

    print(
        login_response.json()
    )


    token = login_response.json()["session_token"]



    session_response = client.get(

        "/auth/session",

        params={

            "token": token

        }

    )


    print()

    print(
        "CURRENT SESSION:"
    )

    print(
        session_response.json()
    )



    data = session_response.json()



    assert data["logged_in"] is True

    assert data["user_id"] == 18



    print()

    print(
        "CURRENT SESSION API PASSED ✅"
    )





if __name__ == "__main__":

    test_current_session_api()