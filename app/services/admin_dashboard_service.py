from sqlalchemy.orm import Session


from app.repositories.admin_dashboard_repository import (

    get_total_paid_commission,

    get_total_releases,

    get_pending_commissions,

    get_failed_commissions,

    get_active_referrers,

    get_earning_referrers

)





def get_dashboard_summary(
    db: Session
):


    return {

        "total_commission_paid":
            get_total_paid_commission(db),


        "total_releases":
            get_total_releases(db),


        "pending_commissions":
            get_pending_commissions(db),


        "failed_commissions":
            get_failed_commissions(db),


        "active_referrers":
            get_active_referrers(db),


        "earning_referrers":
            get_earning_referrers(db)

    }