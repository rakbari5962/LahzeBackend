from sqlalchemy.orm import Session


from app.repositories.admin_release_error_repository import (
    get_failed_release_history
)





def get_release_errors_admin(
    db: Session
):


    errors = get_failed_release_history(
        db
    )


    items = []


    for error in errors:


        items.append(

            {
                "reward_event_id": error.id,

                "user_id": error.user_id,

                "booking_id": error.booking_id,

                "amount": error.amount,

                "type": error.type,

                "status": error.status,

                "transaction_id": error.transaction_id,

                "created_at": error.created_at

            }

        )


    return {

        "count": len(items),

        "items": items

    }