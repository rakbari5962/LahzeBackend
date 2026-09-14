from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.business_service import (
    BusinessServiceCreate,
    BusinessServiceResponse
)


from app.services.business_services_service import (
    add_business_service,
    list_business_services,
    get_service,
    update_business_service,
    deactivate_business_service
)





router = APIRouter(

    prefix="/businesses",

    tags=["Business Services"]

)









@router.get(

    "/{business_id}/services",

    response_model=list[BusinessServiceResponse]

)
def get_services(

    business_id: int,

    db: Session = Depends(get_db)

):


    return list_business_services(

        db=db,

        business_id=business_id

    )









@router.post(

    "/{business_id}/services",

    response_model=BusinessServiceResponse

)
def create_service(

    business_id: int,

    service: BusinessServiceCreate,

    db: Session = Depends(get_db)

):


    return add_business_service(

        db=db,

        business_id=business_id,

        service=service

    )









@router.get(

    "/services/{service_id}",

    response_model=BusinessServiceResponse

)
def get_single_service(

    service_id: int,

    db: Session = Depends(get_db)

):


    return get_service(

        db=db,

        service_id=service_id

    )









@router.patch(

    "/services/{service_id}",

    response_model=BusinessServiceResponse

)
def update_service(

    service_id: int,

    service: BusinessServiceCreate,

    db: Session = Depends(get_db)

):


    return update_business_service(

        db=db,

        service_id=service_id,

        data=service

    )









@router.delete(

    "/services/{service_id}",

    response_model=BusinessServiceResponse

)
def delete_service(

    service_id: int,

    db: Session = Depends(get_db)

):


    return deactivate_business_service(

        db=db,

        service_id=service_id

    )