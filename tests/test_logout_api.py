from fastapi.testclient import TestClient

from unittest.mock import patch, Mock

from app.main import app


client = TestClient(app)



def test_logout_api():


    print(
        "LOGOUT API TEST"
    )

    print(
        "==============="
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



    session_before = client.get(

        "/auth/session",

        params={

            "token": token

        }

    )


    print()

    print(
        "BEFORE LOGOUT:"
    )

    print(
        session_before.json()
    )



    assert session_before.json()["logged_in"] is True



    logout = client.post(

        "/auth/logout",

        params={

            "token": token

        }

    )


    print()

    print(
        "LOGOUT:"
    )

    print(
        logout.json()
    )



    session_after = client.get(

        "/auth/session",

        params={

            "token": token

        }

    )


    print()

    print(
        "AFTER LOGOUT:"
    )

    print(
        session_after.json()
    )



    assert session_after.json()["logged_in"] is False



    print()

    print(
        "LOGOUT API PASSED ✅"
    )





if __name__ == "__main__":

    test_logout_api()