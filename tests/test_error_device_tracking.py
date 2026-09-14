from fastapi.testclient import TestClient


from app.app.main import app


from app.database.database import SessionLocal


from app.models.error_occurrence import ErrorOccurrence





client = TestClient(app)





def test_error_device_tracking():


    print(
        "ERROR DEVICE TRACKING TEST"
    )

    print(
        "========================="
    )



    response = client.get(

        "/test-error",

        headers={

            "X-Platform": "ANDROID",

            "X-Device-Model": "Galaxy A54",

            "X-OS-Version": "Android 15",

            "X-App-Version": "1.0.7"

        }

    )



    print()

    print(
        "STATUS:"
    )

    print(
        response.status_code
    )


    print(
        response.json()
    )





    db = SessionLocal()



    occurrence = db.query(

        ErrorOccurrence

    ).order_by(

        ErrorOccurrence.id.desc()

    ).first()



    print()

    print(
        "LATEST OCCURRENCE DEVICE INFO:"
    )



    print(

        occurrence.device_info

    )



    db.close()



    assert occurrence.device_info["platform"] == "ANDROID"

    assert occurrence.device_info["device_model"] == "Galaxy A54"

    assert occurrence.device_info["app_version"] == "1.0.7"



    print()

    print(
        "DEVICE TRACKING PASSED ✅"
    )





if __name__ == "__main__":

    test_error_device_tracking()