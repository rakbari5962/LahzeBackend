from sqlalchemy.orm import Session


from fastapi import HTTPException


from app.models.business import Business
from app.models.business_service import BusinessService


from app.schemas.business_service import BusinessServiceCreate





def create_business_service(

    db: Session,

    business_id: int,

    service: BusinessServiceCreate,

    commit: bool = True

):


    business = (
        db.query(Business)
        .filter(Business.id == business_id)
        .with_for_update()
        .first()
    )

    if not business:
        raise HTTPException(status_code=404, detail="BUSINESS_NOT_FOUND")

    if business.is_deleted:
        raise HTTPException(status_code=409, detail="BUSINESS_DELETED")

    db_service = BusinessService(

        business_id=business_id,

        name=service.name,

        category=service.category,

        duration_minutes=service.duration_minutes,

        price=service.price,

        description=service.description

    )


    db.add(db_service)

    if commit:
        db.commit()
        db.refresh(db_service)
    else:
        db.flush()


    return db_service







def get_business_services(

    db: Session,

    business_id: int

):


    return db.query(BusinessService).filter(

        BusinessService.business_id == business_id,

        BusinessService.is_active == True

    ).all()








def get_business_service(

    db: Session,

    service_id: int

):


    return db.query(BusinessService).filter(

        BusinessService.id == service_id

    ).first()








def deactivate_business_service(

    db: Session,

    service_id: int

):


    service = get_business_service(

        db,

        service_id

    )


    if not service:

        raise Exception(

            "Service not found"

        )



    service.is_active = False


    db.commit()

    db.refresh(service)


    return service