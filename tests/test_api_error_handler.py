from fastapi.testclient import TestClient


from app.app.main import app


from app.database.database import SessionLocal

from app.models.error_occurrence import ErrorOccurrence



client = TestClient(app)



def test_error_handler():


    print(
        "API ERROR HANDLER TEST"
    )

    print(
        "====================="
    )


    response = client.get(
        "/test-error"
    )


    print(
        "STATUS:"
    )

    print(
        response.status_code
    )


    print(
        "RESPONSE:"
    )

    print(
        response.json()
    )



    db = SessionLocal()


    error = db.query(
        ErrorOccurrence
    ).order_by(
        ErrorOccurrence.id.desc()
    ).first()



    print()

    print(
        "LATEST ERROR OCCURRENCE:"
    )


    print(
        {
            "id": error.id,
            "code": error.error_code,
            "action": error.action,
            "context": error.context
        }
    )


    db.close()



if __name__ == "__main__":

    test_error_handler()