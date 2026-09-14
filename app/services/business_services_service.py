from sqlalchemy.orm import Session


from app.repositories.business_service_repository import (

    create_business_service,

    get_business_services,

    get_business_service

)


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



    service.is_active = False



    db.commit()

    db.refresh(service)



    return service