from sqlalchemy.orm import Session

from app.repositories.business_category_repository import (
    get_categories
)



def suggest_business_category(
    db: Session,
    name: str,
    description: str | None,
    services: list[str]
):

    categories = get_categories(db)


    text = (
        name
        + " "
        + (description or "")
        + " "
        + " ".join(services)
    )


    text = text.lower()



    for category in categories:


        if (
            "زیبایی" in category.name
            and
            (
                "مو" in text
                or
                "ناخن" in text
                or
                "کراتین" in text
            )
        ):

            return {
                "category_id": category.id,
                "category_name": category.name,
                "confidence": 95,
                "reason":
                "خدمات وارد شده مرتبط با حوزه زیبایی است"
            }



    return {
        "category_id": categories[0].id,
        "category_name": categories[0].name,
        "confidence": 50,
        "reason":
        "نیاز به بررسی بیشتر دارد"
    }