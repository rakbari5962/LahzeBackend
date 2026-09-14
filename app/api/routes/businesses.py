from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.business import (
    BusinessCreate,
    BusinessResponse,
    BusinessLocationUpdate
)


from app.schemas.ai_category_suggestion import (
    CategorySuggestionRequest
)


from app.schemas.category_suggestion import (
    CategorySuggestionResponse
)


from app.repositories.business_repository import (
    get_business,
    update_business_location
)


from app.services.business_service import (
    create_business
)


from app.services.session_service import (
    get_login_session
)


from app.services.category_suggestion_service import (
    create_ai_category_suggestion
)



router = APIRouter(

    prefix="/businesses",

    tags=["Businesses"]

)





@router.post(

    "/",

    response_model=BusinessResponse

)
def create_new_business(

    business: BusinessCreate,

    token: str = Query(...),

    db: Session = Depends(get_db)

):


    session = get_login_session(

        db=db,

        token=token

    )


    if not session:

        raise Exception(

            "User not logged in"

        )



    return create_business(

        db,

        business,

        session.user_id

    )







@router.patch(

    "/{business_id}/location",

    response_model=BusinessResponse

)
def update_location(

    business_id: int,

    location: BusinessLocationUpdate,

    token: str = Query(...),

    db: Session = Depends(get_db)

):


    session = get_login_session(

        db=db,

        token=token

    )


    if not session:

        raise Exception(

            "User not logged in"

        )



    business = get_business(

        db,

        business_id

    )


    if not business:

        raise Exception(

            "Business not found"

        )



    if business.owner_user_id != session.user_id:

        raise Exception(

            "You are not the owner of this business"

        )



    return update_business_location(

        db=db,

        business_id=business_id,

        latitude=location.latitude,

        longitude=location.longitude,

        address=location.address

    )









@router.post(

    "/{business_id}/suggest-category",

    response_model=CategorySuggestionResponse

)
def suggest_business_category(

    business_id: int,

    data: CategorySuggestionRequest,

    db: Session = Depends(get_db)

):


    return create_ai_category_suggestion(

        db=db,

        business_id=business_id,

        business_name=data.business_name,

        services=data.services,

        description=data.description

    )









@router.get(

    "/{business_id}",

    response_model=BusinessResponse

)
def read_business(

    business_id: int,

    db: Session = Depends(get_db)

):


    return get_business(

        db,

        business_id

    )