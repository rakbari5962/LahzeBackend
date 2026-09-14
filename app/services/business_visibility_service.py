from sqlalchemy.orm import Session


from app.models.business import Business

from app.models.business_service import BusinessService

from app.models.city import City





def get_business_visibility_detail(

    db: Session,

    business_id: int

):


    business = db.query(Business).filter(

        Business.id == business_id

    ).first()



    if not business:

        return {

            "business_id": business_id,

            "visible": False,

            "checks": {},

            "reason": "BUSINESS_NOT_FOUND"

        }



    checks = {

        "status_active": False,

        "not_deleted": False,

        "has_active_service": False,

        "city_active": False

    }



    reasons = []



    # شرط ۱:
    # وضعیت ACTIVE

    if business.status == "ACTIVE":

        checks["status_active"] = True

    else:

        reasons.append(

            "STATUS_NOT_ACTIVE"

        )



    # شرط ۲:
    # حذف نشده باشد

    if not business.is_deleted:

        checks["not_deleted"] = True

    else:

        reasons.append(

            "BUSINESS_DELETED"

        )



    # شرط ۳:
    # سرویس فعال داشته باشد

    active_service = db.query(BusinessService).filter(

        BusinessService.business_id == business_id,

        BusinessService.is_active == True

    ).first()



    if active_service:

        checks["has_active_service"] = True

    else:

        reasons.append(

            "NO_ACTIVE_SERVICE"

        )



    # شرط ۴:
    # شهر فعال باشد

    if business.city_id:

        city = db.query(City).filter(

            City.id == business.city_id

        ).first()



        if city and city.is_active:

            checks["city_active"] = True

        else:

            reasons.append(

                "CITY_NOT_ACTIVE"

            )

    else:

        reasons.append(

            "CITY_NOT_FOUND"

        )



    visible = all(

        checks.values()

    )



    return {

        "business_id": business_id,

        "visible": visible,

        "checks": checks,

        "reason": None if visible else reasons

    }





# سازگاری با کد قبلی

def is_business_visible(

    db: Session,

    business_id: int

):

    result = get_business_visibility_detail(

        db,

        business_id

    )

    return result["visible"]