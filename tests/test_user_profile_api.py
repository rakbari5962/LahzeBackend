from fastapi.testclient import TestClient

from unittest.mock import patch, Mock

from app.main import app

from app.database.database import SessionLocal

from app.models.otp_request import OTPRequest



client = TestClient(app)



def test_user_profile_api():


    print(
        "USER PROFILE API TEST"
    )

    print(
        "===================="
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


        client.post(

            "/auth/request-otp",

            params={

                "phone_number": phone_number

            }

        )



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



    login = client.post(

        "/auth/verify-otp",

        params={

            "phone_number": phone_number,

            "code": code

        }

    )


    token = login.json()["session_token"]



    print()

    print(
        "TOKEN:"
    )

    print(token)



    profile = client.get(

        "/users/me",

        params={

            "token": token

        }

    )



    print()

    print(
        "PROFILE:"
    )

    print(
        profile.json()
    )



    assert profile.status_code == 200


    data = profile.json()


    assert data["phone_number"] == phone_number


    print()

    print(
        "USER PROFILE API PASSED ✅"
    )





if __name__ == "__main__":

    test_user_profile_api()