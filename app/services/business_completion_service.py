from sqlalchemy.orm import Session


from app.models.business import Business

from app.models.business_service import BusinessService


from app.services.business_status_service import (
    update_business_status
)







def calculate_business_completion(

    db: Session,

    business_id: int

):


    business = db.query(Business).filter(

        Business.id == business_id

    ).first()



    if not business:

        raise Exception(

            "Business not found"

        )



    completed_items = []

    missing_items = []


    score = 0





    # اطلاعات پایه

    if (

        business.name

        and business.province_id

        and business.city_id

    ):

        score += 20

        completed_items.append(

            "basic_info"

        )

    else:

        missing_items.append(

            "basic_info"

        )





    # شماره تماس

    if business.phone:

        score += 20

        completed_items.append(

            "phone"

        )

    else:

        missing_items.append(

            "phone"

        )





    # توضیحات

    if business.description:

        score += 15

        completed_items.append(

            "description"

        )

    else:

        missing_items.append(

            "description"

        )





    # دسته بندی

    if business.category_id:

        score += 20

        completed_items.append(

            "category"

        )

    else:

        missing_items.append(

            "category"

        )





    # خدمات

    service_exists = db.query(

        BusinessService

    ).filter(

        BusinessService.business_id == business_id,

        BusinessService.is_active == True

    ).first()



    if service_exists:

        score += 15

        completed_items.append(

            "services"

        )

    else:

        missing_items.append(

            "services"

        )





    # موقعیت

    if (

        business.latitude

        and business.longitude

        and business.address

    ):

        score += 10

        completed_items.append(

            "location"

        )

    else:

        missing_items.append(

            "location"

        )





    # به روزرسانی وضعیت کسب و کار

    update_business_status(

        db=db,

        business_id=business_id,

        completion_percentage=score

    )





    return {

        "business_id": business_id,

        "completion_percentage": score,

        "is_complete": score == 100,

        "missing_items": missing_items,

        "completed_items": completed_items

    }