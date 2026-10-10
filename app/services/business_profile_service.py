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


from app.repositories.business_repository import (
    get_business,
    update_business_profile
)

from app.repositories.location_repository import (
    get_city_by_province
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
        raise Exception("Business not found")

    return business


def update_profile(
    db: Session,
    business_id: int,
    updates: dict
):
    province_present = "province_id" in updates
    city_present = "city_id" in updates

    # Province and City must always be changed together.
    if province_present != city_present:
        raise Exception(
            "Province and city must be provided together"
        )

    if province_present and city_present:

        province_id = updates["province_id"]
        city_id = updates["city_id"]

        if province_id is None or city_id is None:
            raise Exception(
                "Province and city are required"
            )

        city = get_city_by_province(
            db=db,
            city_id=city_id,
            province_id=province_id
        )

        if not city:
            raise Exception(
                "City does not belong to the selected province"
            )

    business = update_business_profile(
        db=db,
        business_id=business_id,
        updates=updates
    )

    if not business:
        raise Exception("Business not found")

    return business