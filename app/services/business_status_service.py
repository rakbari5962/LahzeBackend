from sqlalchemy.orm import Session


from app.models.business import Business


from app.core.constants.business_status import (
    BusinessStatus
)



def update_business_status(

    db: Session,

    business_id: int,

    completion_percentage: int

):


    business = db.query(Business).filter(

        Business.id == business_id

    ).first()



    if not business:

        raise Exception(

            "Business not found"

        )



    if completion_percentage < 50:

        business.status = BusinessStatus.DRAFT



    elif completion_percentage < 100:

        business.status = BusinessStatus.PROFILE_INCOMPLETE



    else:

        business.status = BusinessStatus.READY





    db.commit()

    db.refresh(business)



    return business