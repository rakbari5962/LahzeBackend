from fastapi.testclient import TestClient


from app.main import app


from app.database.database import SessionLocal


from app.models.user import User


from app.models.user_device import UserDevice



client = TestClient(app)




def test_device_api():


    print(
        "DEVICE API TEST"
    )

    print(
        "==============="
    )


    db = SessionLocal()



    # CREATE TEST USER

    user = User(

        phone_number="09990000003",

        role="CUSTOMER"

    )


    db.add(user)

    db.commit()

    db.refresh(user)



    user_id = user.id



    db.close()



    print()

    print(
        "USER ID:",
        user_id
    )




    # 1) REGISTER DEVICE


    response = client.post(

        "/devices/register",

        params={

            "user_id": user_id,

            "device_id": "API_DEVICE_001",

            "platform": "ANDROID",

            "device_model": "Galaxy A54",

            "os_version": "Android 15",

            "app_version": "1.0.7"

        }

    )


    print()

    print(
        "REGISTER:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )


    assert response.status_code == 200




    # 2) REGISTER SAME DEVICE AGAIN


    response = client.post(

        "/devices/register",

        params={

            "user_id": user_id,

            "device_id": "API_DEVICE_001",

            "platform": "ANDROID",

            "device_model": "Galaxy A54",

            "os_version": "Android 15",

            "app_version": "1.0.8"

        }

    )


    print()

    print(
        "UPDATE SAME DEVICE:"
    )

    print(
        response.json()
    )


    assert response.json()["app_version"] == "1.0.8"




    # 3) GET DEVICES


    response = client.get(

        "/devices/me",

        params={

            "user_id": user_id

        }

    )


    print()

    print(
        "MY DEVICES:"
    )

    print(
        response.json()
    )


    assert len(response.json()) == 1




    # 4) LOGOUT


    response = client.patch(

        "/devices/API_DEVICE_001/logout"

    )


    print()

    print(
        "LOGOUT:"
    )

    print(
        response.json()
    )


    assert response.json()["is_active"] is False




    print()

    print(
        "DEVICE API PASSED ✅"
    )





if __name__ == "__main__":

    test_device_api()