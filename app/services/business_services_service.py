from sqlalchemy.orm import Session


from fastapi import HTTPException


from app.repositories.business_service_repository import (

    create_business_service,

    get_business_services,

    get_business_service

)


from app.models.business import Business
from app.models.business_service import BusinessService


from app.schemas.business_service import BusinessServiceCreate







def add_business_service(

    db: Session,

    business_id: int,

    service: BusinessServiceCreate

):


    return create_business_service(

        db=db,

        business_id=business_id,

        service=service

    )









def list_business_services(

    db: Session,

    business_id: int

):


    return get_business_services(

        db=db,

        business_id=business_id

    )









def get_service(

    db: Session,

    service_id: int

):


    service = get_business_service(

        db=db,

        service_id=service_id

    )


    if not service:

        raise Exception(

            "Service not found"

        )


    return service









def update_business_service(

    db: Session,

    service_id: int,

    data: BusinessServiceCreate

):


    service = get_business_service(

        db=db,

        service_id=service_id

    )


    if not service:

        raise Exception(

            "Service not found"

        )


    business = (
        db.query(Business)
        .filter(Business.id == service.business_id)
        .with_for_update()
        .first()
    )

    if not business:
        raise HTTPException(status_code=404, detail="BUSINESS_NOT_FOUND")

    if business.is_deleted:
        raise HTTPException(status_code=409, detail="BUSINESS_DELETED")



    service.name = data.name

    service.category = data.category

    service.duration_minutes = data.duration_minutes

    service.price = data.price

    service.description = data.description



    db.commit()

    db.refresh(service)



    return service









def deactivate_business_service(

    db: Session,

    service_id: int

):


    service = get_business_service(

        db=db,

        service_id=service_id

    )


    if not service:

        raise Exception(

            "Service not found"

        )


    business = (
        db.query(Business)
        .filter(Business.id == service.business_id)
        .with_for_update()
        .first()
    )

    if not business:
        raise HTTPException(status_code=404, detail="BUSINESS_NOT_FOUND")

    if business.is_deleted:
        raise HTTPException(status_code=409, detail="BUSINESS_DELETED")



    service.is_active = False



    db.commit()

    db.refresh(service)



    return service