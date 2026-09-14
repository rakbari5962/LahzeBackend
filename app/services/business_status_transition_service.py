from app.schemas.business_status import BusinessStatusEnum





ALLOWED_TRANSITIONS = {


    BusinessStatusEnum.DRAFT: [

        BusinessStatusEnum.PROFILE_INCOMPLETE

    ],



    BusinessStatusEnum.PROFILE_INCOMPLETE: [

        BusinessStatusEnum.READY

    ],



    BusinessStatusEnum.READY: [

        BusinessStatusEnum.ACTIVE

    ],



    BusinessStatusEnum.ACTIVE: [

        BusinessStatusEnum.SUSPENDED

    ],



    BusinessStatusEnum.SUSPENDED: [

        BusinessStatusEnum.ACTIVE

    ]

}







def can_transition(

    current_status: BusinessStatusEnum,

    new_status: BusinessStatusEnum

):


    allowed = ALLOWED_TRANSITIONS.get(

        current_status,

        []

    )


    return new_status in allowed