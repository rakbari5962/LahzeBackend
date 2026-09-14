from sqlalchemy.orm import Session


from app.models.business import Business


from app.services.business_completion_service import (
    calculate_business_completion
)


from app.schemas.business_status import (
    BusinessStatusEnum
)





def evaluate_business_status(

    db: Session,

    business_id: int

):

    business = db.query(Business).filter(

        Business.id == business_id

    ).first()


    if not business:

        raise Exception(
            "Business not found"
        )


    completion = calculate_business_completion(

        db=db,

        business_id=business_id

    )


    if completion["completion_percentage"] == 100:

        suggested_status = BusinessStatusEnum.READY


    else:

        suggested_status = BusinessStatusEnum.PROFILE_INCOMPLETE



    return {

        "business_id": business_id,

        "current_status": business.status,

        "suggested_status": suggested_status.value,

        "completion_percentage": completion["completion_percentage"]

    }