from sqlalchemy.orm import Session


from app.repositories.business_repository import (

    get_business,

    update_business_profile

)





def get_business_profile(

    db: Session,

    business_id: int

):


    business = get_business(

        db=db,

        business_id=business_id

    )


    if not business:

        raise Exception(

            "Business not found"

        )


    return business







def update_profile(

    db: Session,

    business_id: int,

    description: str | None = None,

    phone: str | None = None

):


    business = update_business_profile(

        db=db,

        business_id=business_id,

        description=description,

        phone=phone

    )


    if not business:

        raise Exception(

            "Business not found"

        )


    return business