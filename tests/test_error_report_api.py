from fastapi.testclient import TestClient


from app.main import app


from app.database.database import SessionLocal


from app.models.error_report import ErrorReport


from app.models.error_occurrence import ErrorOccurrence



client = TestClient(app)





def test_error_report_api():


    print(
        "ERROR REPORT DESCRIPTION FLOW TEST"
    )

    print(
        "================================="
    )



    db = SessionLocal()



    occurrence = ErrorOccurrence(

        error_code=500,

        action="BOOKING_COMPLETE",

        context={

            "reason": "ESCROW_LOW_BALANCE",

            "booking_id": 8,

            "business_id": 1,

            "escrow_balance": 0,

            "required_amount": 10000

        }

    )


    db.add(
        occurrence
    )

    db.commit()


    db.refresh(
        occurrence
    )



    occurrence_id = occurrence.id



    print()

    print(
        "CREATED OCCURRENCE:",
        occurrence_id
    )



    db.close()



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
        "STATUS:"
    )

    print(
        response.status_code
    )



    print()

    print(
        "RESPONSE:"
    )

    print(
        response.json()
    )



    db = SessionLocal()



    report = db.query(
        ErrorReport
    ).order_by(
        ErrorReport.id.desc()
    ).first()



    print()

    print(
        "LATEST ERROR REPORT:"
    )


    print(

        {

            "id": report.id,

            "occurrence_id":
                report.occurrence_id,

            "system_description":
                report.system_description,

            "user_message":
                report.user_message,

            "status":
                report.status

        }

    )



    assert report.system_description is not None


    db.close()



    print()

    print(
        "ERROR REPORT DESCRIPTION FLOW PASSED ✅"
    )




if __name__ == "__main__":

    test_error_report_api()