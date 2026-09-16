from sqlalchemy.orm import Session

from app.models.business_priority_access import BusinessPriorityAccess



def create_priority_access(
    db: Session,
    business_id: int,
    user_id: int,
    access_type: str,
    source_id: int | None = None
):

    priority_access = BusinessPriorityAccess(

        business_id=business_id,

        user_id=user_id,

        type=access_type,

        source_id=source_id,

        status="ACTIVE"

    )


    db.add(priority_access)

    db.commit()

    db.refresh(priority_access)


    return priority_access





def get_business_priority_accesses(
    db: Session,
    business_id: int
):

    return (

        db.query(BusinessPriorityAccess)

        .filter(

            BusinessPriorityAccess.business_id == business_id

        )

        .all()

    )





def get_first_customer_access(
    db: Session,
    business_id: int
):

    return (

        db.query(BusinessPriorityAccess)

        .filter(

            BusinessPriorityAccess.business_id == business_id,

            BusinessPriorityAccess.type == "FIRST_CUSTOMER",

            BusinessPriorityAccess.status == "ACTIVE"

        )

        .first()

    )





def has_first_customer_access(
    db: Session,
    business_id: int
):

    access = get_first_customer_access(

        db=db,

        business_id=business_id

    )


    return access is not None