from sqlalchemy.orm import Session


from app.repositories.category_suggestion_repository import (

    create_category_suggestion,

    get_category_suggestion,

    approve_category_suggestion_with_business_update,

    reject_category_suggestion

)


from app.repositories.business_repository import (

    get_business

)


from app.repositories.business_service_repository import (

    get_business_services

)


from app.repositories.category_ai_history_repository import (

    create_category_ai_history

)


from app.services.ai_category_service import (

    suggest_category

)





def create_suggestion(

    db: Session,

    business_id: int,

    suggested_category_id: int,

    confidence: int,

    reason: str | None = None

):


    business = get_business(

        db,

        business_id

    )


    if not business:

        raise Exception(

            "Business not found"

        )



    return create_category_suggestion(

        db=db,

        business_id=business_id,

        suggested_category_id=suggested_category_id,

        confidence=confidence,

        reason=reason

    )









def create_ai_category_suggestion(

    db: Session,

    business_id: int,

    business_name: str,

    services: list[str],

    description: str | None = None

):


    business = get_business(

        db,

        business_id

    )


    if not business:

        raise Exception(

            "Business not found"

        )



    # دریافت خدمات واقعی ذخیره شده در دیتابیس

    business_services = get_business_services(

        db=db,

        business_id=business_id

    )



    service_names = [

        service.name

        for service in business_services

    ]



    # اگر هنوز سرویسی در دیتابیس نبود

    # از ورودی اولیه استفاده شود

    if not service_names:

        service_names = services



    ai_result = suggest_category(

        db=db,

        business_name=business_name,

        services=service_names,

        description=description

    )



    if not ai_result.get("category_id"):

        return None





    return create_category_suggestion(

        db=db,

        business_id=business_id,

        suggested_category_id=ai_result["category_id"],

        confidence=ai_result["confidence"],

        reason=ai_result["reason"],

        input_snapshot={

            "business_name": business_name,

            "services": service_names,

            "description": description

        }

    )









def get_suggestion(

    db: Session,

    suggestion_id: int

):


    suggestion = get_category_suggestion(

        db,

        suggestion_id

    )


    if not suggestion:

        raise Exception(

            "Suggestion not found"

        )


    return suggestion











def approve_suggestion(

    db: Session,

    suggestion_id: int

):


    suggestion = get_category_suggestion(

        db,

        suggestion_id

    )


    if not suggestion:

        raise Exception(

            "Suggestion not found"

        )



    result = approve_category_suggestion_with_business_update(

        db,

        suggestion

    )



    create_category_ai_history(

        db=db,

        business_id=suggestion.business_id,

        suggestion_id=suggestion.id,

        suggested_category_id=suggestion.suggested_category_id,

        action="ACCEPTED",

        confidence=suggestion.confidence,

        input_snapshot=suggestion.input_snapshot

    )



    return result











def reject_suggestion(

    db: Session,

    suggestion_id: int

):


    suggestion = get_category_suggestion(

        db,

        suggestion_id

    )


    if not suggestion:

        raise Exception(

            "Suggestion not found"

        )



    result = reject_category_suggestion(

        db,

        suggestion

    )



    create_category_ai_history(

        db=db,

        business_id=suggestion.business_id,

        suggestion_id=suggestion.id,

        suggested_category_id=suggestion.suggested_category_id,

        action="REJECTED",

        confidence=suggestion.confidence,

        input_snapshot=suggestion.input_snapshot

    )



    return result