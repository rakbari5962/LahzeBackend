from app.database.database import SessionLocal

from app.services.settlement_service import (
    settle_payment
)

from app.models.account import Account

from app.models.error_occurrence import ErrorOccurrence



def test_settlement_error_capture():

    db = SessionLocal()


    print(
        "SETTLEMENT ERROR CAPTURE TEST"
    )

    print(
        "============================"
    )


    # صفر کردن Escrow

    escrow = db.query(Account).filter(
        Account.account_type == "ESCROW"
    ).first()


    escrow.balance = 0

    db.commit()



    print(
        "ESCROW BALANCE:",
        escrow.balance
    )



    result = settle_payment(

        db=db,

        booking_id=999,

        business_id=1,

        amount=10000

    )


    print()

    print(
        "SETTLEMENT RESULT:"
    )

    print(
        result
    )



    error = db.query(
        ErrorOccurrence
    ).order_by(
        ErrorOccurrence.id.desc()
    ).first()



    print()

    print(
        "LATEST ERROR:"
    )


    print(
        {
            "id": error.id,
            "error_code": error.error_code,
            "action": error.action,
            "context": error.context
        }
    )


    db.close()



if __name__ == "__main__":

    test_settlement_error_capture()