from datetime import datetime


from sqlalchemy.orm import Session


from app.models.opportunity import Opportunity


from app.schemas.opportunity_status import (
    OpportunityStatusEnum
)





def expire_old_opportunities(

    db: Session

):


    now = datetime.now()



    expired_opportunities = db.query(

        Opportunity

    ).filter(

        Opportunity.status == OpportunityStatusEnum.ACTIVE.value,

        Opportunity.end_time <= now

    ).all()



    updated_count = 0



    for opportunity in expired_opportunities:


        opportunity.status = OpportunityStatusEnum.EXPIRED.value


        updated_count += 1



    db.commit()



    return {

        "expired_count": updated_count

    }