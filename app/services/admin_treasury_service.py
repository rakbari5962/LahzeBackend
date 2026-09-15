from sqlalchemy.orm import Session


from app.repositories.admin_treasury_repository import (

    get_treasury_balance,

    get_total_commission_paid,

    get_transaction_count

)





def get_treasury_health(
    db: Session
):


    return {

        "treasury_balance":
            get_treasury_balance(db),


        "total_commission_paid":
            get_total_commission_paid(db),


        "transaction_count":
            get_transaction_count(db)

    }