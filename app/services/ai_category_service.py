from sqlalchemy.orm import Session

from app.repositories.business_category_repository import (
    get_categories
)



def suggest_category(
    db: Session,
    business_name: str,
    services: list[str],
    description: str | None = None
):

    categories = get_categories(db)


    text = " ".join(
        [
            business_name,
            *services,
            description or ""
        ]
    ).lower()



    keyword_map = {

        "beauty": [
            "مو",
            "آرایش",
            "زیبایی",
            "ناخن",
            "مژه",
            "ابرو",
            "پوست",
            "کراتین",
            "رنگ"
        ],


        "restaurant": [
            "رستوران",
            "کافه",
            "غذا",
            "قهوه",
            "فست فود",
            "کیک"
        ],


        "health": [
            "پزشک",
            "کلینیک",
            "درمان",
            "دندان",
            "سلامت"
        ],


        "home-services": [
            "تعمیر",
            "کولر",
            "لوله",
            "برق",
            "خانه"
        ],


        "education": [
            "آموزش",
            "کلاس",
            "دوره",
            "زبان",
            "موسیقی"
        ],


        "fitness": [
            "باشگاه",
            "ورزش",
            "بدنسازی",
            "یوگا"
        ],


        "automotive": [
            "خودرو",
            "ماشین",
            "موتور",
            "تعمیرگاه"
        ],


        "retail": [
            "فروشگاه",
            "فروش",
            "محصول",
            "لباس"
        ]

    }



    scores = {}


    for category_slug, keywords in keyword_map.items():

        score = 0

        for keyword in keywords:

            if keyword in text:

                score += 1


        scores[category_slug] = score



    best_slug = max(

        scores,

        key=scores.get

    )



    best_score = scores[best_slug]



    if best_score == 0:

        return {

            "category_id": None,

            "category_name": None,

            "confidence": 0,

            "reason": "داده کافی برای تشخیص دسته وجود ندارد"

        }



    category = next(

        (

            item

            for item in categories

            if item.slug == best_slug

        ),

        None

    )



    confidence = min(

        best_score * 20,

        95

    )



    return {

        "category_id": category.id,

        "category_name": category.name,

        "confidence": confidence,

        "reason": f"بر اساس خدمات و نام کسب‌وکار، کلمات مرتبط با {category.name} شناسایی شد"

    }