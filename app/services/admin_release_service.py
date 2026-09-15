from sqlalchemy.orm import Session


from app.repositories.admin_release_repository import (
    get_release_history
)





def get_release_history_admin(
    db: Session
):


    releases = get_release_history(
        db
    )


    items = []


    for release in releases:


        items.append(

            {
                "reward_event_id": release.id,

                "user_id": release.user_id,

                "booking_id": release.booking_id,

                "amount": release.amount,

                "type": release.type,

                "status": release.status,

                "transaction_id": release.transaction_id,

                "created_at": release.created_at

            }

        )



    return {

        "count": len(items),

        "items": items

    }