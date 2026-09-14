from sqlalchemy.orm import Session


from app.models.business import Business


from app.schemas.business_status import (
    BusinessStatusEnum
)


from app.services.business_completion_service import (
    calculate_business_completion
)


from app.services.business_status_management_service import (
    update_business_status_manually
)







def auto_update_business_status(

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



    current_status = BusinessStatusEnum(

        business.status

    )



    suggested_status = current_status





    # اگر اطلاعات کامل شد

    if completion["completion_percentage"] == 100:


        if current_status == BusinessStatusEnum.PROFILE_INCOMPLETE:

            suggested_status = BusinessStatusEnum.READY



        elif current_status == BusinessStatusEnum.READY:

            suggested_status = BusinessStatusEnum.ACTIVE



    else:


        if current_status == BusinessStatusEnum.DRAFT:

            suggested_status = BusinessStatusEnum.PROFILE_INCOMPLETE





    # اگر تغییری نیاز نیست

    if suggested_status == current_status:

        return {

            "business_id": business_id,

            "old_status": current_status.value,

            "new_status": current_status.value,

            "changed": False,

            "completion_percentage": completion["completion_percentage"]

        }





    updated_business = update_business_status_manually(

        db=db,

        business_id=business_id,

        status=suggested_status

    )





    return {

        "business_id": business_id,

        "old_status": current_status.value,

        "new_status": updated_business.status,

        "changed": True,

        "completion_percentage": completion["completion_percentage"]

    }