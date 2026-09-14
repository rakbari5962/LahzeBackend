from fastapi.testclient import TestClient

import time


from app.main import app


from app.database.database import SessionLocal


from app.models.user import User


from app.models.error_occurrence import ErrorOccurrence



client = TestClient(app)





def test_admin_device_analytics():


    print(
        "ADMIN DEVICE ANALYTICS TEST"
    )

    print(
        "=========================="
    )



    db = SessionLocal()



    # CREATE USER WITH UNIQUE PHONE

    user = User(

        phone_number=f"0999{int(time.time())}",

        role="CUSTOMER"

    )


    db.add(user)

    db.commit()

    db.refresh(user)



    user_id = user.id



    print()

    print(
        "USER ID:",
        user_id
    )





    # CREATE DEVICE THROUGH API


    response = client.post(

        "/devices/register",

        params={

            "user_id": user_id,

            "device_id": f"ANALYTICS_DEVICE_{int(time.time())}",

            "platform": "ANDROID",

            "device_model": "Galaxy S24",

            "os_version": "Android 15",

            "app_version": "2.0.0"

        }

    )



    print()

    print(
        "DEVICE REGISTER:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )


    assert response.status_code == 200



    device_id = response.json()["device_id"]





    # CREATE ERROR OCCURRENCE


    occurrence = ErrorOccurrence(

        error_code=500,

        user_id=user_id,

        action="BOOKING_COMPLETE",

        device_info={

            "platform": "ANDROID",

            "device_model": "Galaxy S24",

            "os_version": "Android 15",

            "app_version": "2.0.0"

        },

        context={

            "test": True,

            "source": "DEVICE_ANALYTICS_TEST"

        }

    )



    db.add(occurrence)

    db.commit()

    db.refresh(occurrence)



    print()

    print(
        "ERROR OCCURRENCE:",
        occurrence.id
    )



    db.close()





    # CALL ADMIN ANALYTICS


    response = client.get(

        "/admin/devices/analytics"

    )



    print()

    print(
        "ADMIN ANALYTICS:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 200



    data = response.json()





    # CHECK ACTIVE DEVICES


    assert data["total_active_devices"] > 0





    # CHECK PLATFORM


    platforms = data["platforms"]


    android = next(

        item

        for item in platforms

        if item["platform"] == "ANDROID"

    )


    assert android["count"] > 0





    # CHECK VERSION


    versions = data["versions"]


    version = next(

        item

        for item in versions

        if item["app_version"] == "2.0.0"

    )


    assert version["count"] > 0





    # CHECK ERROR DEVICE ANALYTICS


    error_devices = data["top_error_devices"]


    galaxy = next(

        item

        for item in error_devices

        if item["device_model"] == "Galaxy S24"

    )


    assert galaxy["error_count"] > 0





    # CHECK ERROR VERSION ANALYTICS


    error_versions = data["problematic_versions"]


    error_version = next(

        item

        for item in error_versions

        if item["app_version"] == "2.0.0"

    )


    assert error_version["error_count"] > 0





    print()

    print(
        "ADMIN DEVICE ANALYTICS PASSED ✅"
    )





if __name__ == "__main__":

    test_admin_device_analytics()