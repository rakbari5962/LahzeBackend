from sqlalchemy.orm import Session


from app.models.business import Business


from app.schemas.business_status import (
    BusinessStatusEnum
)


from app.services.business_status_transition_service import (
    can_transition
)


from app.core.errors.exceptions import (
    LahzeException
)


from app.core.errors.error_codes import (
    ErrorCodes
)







def update_business_status_manually(

    db: Session,

    business_id: int,

    status: BusinessStatusEnum

):


    business = db.query(Business).filter(

        Business.id == business_id

    ).first()



    if not business:

        raise LahzeException(

            error_code=ErrorCodes.UNKNOWN_ERROR,

            message="Business not found",

            context={

                "business_id": business_id

            }

        )



    if not isinstance(status, BusinessStatusEnum):

        raise LahzeException(

            error_code=ErrorCodes.INVALID_BUSINESS_STATUS_TRANSITION,

            message="Invalid business status",

            context={

                "business_id": business_id,

                "requested_status": str(status)

            }

        )



    current_status = BusinessStatusEnum(

        business.status

    )





    # اگر وضعیت جدید با وضعیت فعلی یکی باشد

    if current_status == status:

        return business





    # بررسی Transition مجاز

    if not can_transition(

        current_status,

        status

    ):

        raise LahzeException(

            error_code=ErrorCodes.INVALID_BUSINESS_STATUS_TRANSITION,

            message="Invalid business status transition",

            context={

                "business_id": business_id,

                "current_status": current_status.value,

                "requested_status": status.value

            }

        )





    business.status = status.value



    db.commit()

    db.refresh(business)



    return business