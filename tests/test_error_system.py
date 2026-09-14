from app.database.database import SessionLocal

from app.services.error_service import record_error



def test_error():

    db = SessionLocal()


    result = record_error(

        db=db,

        error_code=500,

        action="SETTLEMENT",

        user_id=3,

        context={

            "booking_id": 8,

            "amount": 3500000,

            "reason": "ESCROW_LOW_BALANCE"

        }

    )


    print(
        "ERROR CREATED"
    )

    print(
        result
    )


    db.close()



if __name__ == "__main__":

    test_error()