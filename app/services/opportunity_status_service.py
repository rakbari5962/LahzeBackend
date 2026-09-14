from datetime import datetime, timezone


from sqlalchemy.orm import Session


from app.models.opportunity import Opportunity


from app.schemas.opportunity_status import (
    OpportunityStatusEnum
)





def update_opportunity_status(

    db: Session,

    opportunity_id: int

):


    opportunity = db.query(Opportunity).filter(

        Opportunity.id == opportunity_id

    ).first()



    if not opportunity:

        raise Exception(

            "Opportunity not found"

        )



    current_status = OpportunityStatusEnum(

        opportunity.status

    )



    # اگر قبلاً منقضی شده، کاری نکن

    if current_status == OpportunityStatusEnum.EXPIRED:

        return opportunity



    now = datetime.now(timezone.utc)



    # پایان زمان فرصت

    if opportunity.end_time <= now:

        opportunity.status = OpportunityStatusEnum.EXPIRED.value



        db.commit()

        db.refresh(opportunity)



    return opportunity