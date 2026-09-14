from fastapi.testclient import TestClient


from app.main import app


from app.database.database import SessionLocal


from app.models.error_occurrence import ErrorOccurrence

from app.models.error_report import ErrorReport





client = TestClient(app)





def test_error_full_flow():


    print(
        "ERROR FULL FLOW TEST"
    )

    print(
        "===================="
    )





    #
    # 1) Mobile App creates error
    #


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
        "CREATE ERROR:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 400



    occurrence_id = response.json()["error"]["occurrence_id"]



    print()

    print(
        "OCCURRENCE ID:",
        occurrence_id
    )







    #
    # 2) Verify ErrorOccurrence
    #


    db = SessionLocal()



    occurrence = db.query(

        ErrorOccurrence

    ).filter(

        ErrorOccurrence.id == occurrence_id

    ).first()



    print()

    print(
        "DEVICE INFO FROM DATABASE:"
    )

    print(
        occurrence.device_info
    )



    assert occurrence.device_info["platform"] == "ANDROID"

    assert occurrence.device_info["device_model"] == "Galaxy A54"

    assert occurrence.device_info["app_version"] == "1.0.7"



    db.close()







    #
    # 3) User submits error report
    #


    response = client.post(

        "/errors/report",

        params={

            "occurrence_id": occurrence_id,

            "user_message":
            "هنگام تکمیل رزرو خطا دریافت کردم"

        }

    )



    print()

    print(
        "CREATE REPORT:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 200



    report_id = response.json()["report_id"]







    #
    # 4) Admin views error
    #


    response = client.get(

        f"/admin/errors/{report_id}",

        headers={

            "X-User-ID": "3"

        }

    )



    print()

    print(
        "ADMIN DETAILS:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 200



    data = response.json()



    assert data["occurrence"]["device_info"]["platform"] == "ANDROID"

    assert data["occurrence"]["device_info"]["device_model"] == "Galaxy A54"

    assert data["occurrence"]["device_info"]["app_version"] == "1.0.7"



    print()

    print(
        "ERROR FULL FLOW PASSED ✅"
    )





if __name__ == "__main__":

    test_error_full_flow()