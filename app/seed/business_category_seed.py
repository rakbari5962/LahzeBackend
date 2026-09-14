from sqlalchemy.orm import Session

from app.models.business_category import BusinessCategory


categories = [

    {
        "name": "زیبایی و مراقبت شخصی",
        "slug": "beauty",
        "description": "خدمات زیبایی، آرایشی و مراقبت شخصی"
    },

    {
        "name": "رستوران و کافه",
        "slug": "restaurant",
        "description": "رستوران‌ها، کافه‌ها و خدمات غذایی"
    },

    {
        "name": "سلامت و درمان",
        "slug": "health",
        "description": "کلینیک‌ها، پزشکان و خدمات درمانی"
    },

    {
        "name": "خدمات منزل و تعمیرات",
        "slug": "home-services",
        "description": "تعمیرات و خدمات مربوط به خانه"
    },

    {
        "name": "آموزش و آموزشگاه",
        "slug": "education",
        "description": "کلاس‌ها و خدمات آموزشی"
    },

    {
        "name": "ورزش و تناسب اندام",
        "slug": "fitness",
        "description": "باشگاه‌ها و خدمات ورزشی"
    },

    {
        "name": "فروشگاه و خرده‌فروشی",
        "slug": "retail",
        "description": "فروشگاه‌ها و کسب‌وکارهای فروش محصول"
    },

    {
        "name": "خودرو و خدمات خودرو",
        "slug": "automotive",
        "description": "تعمیرات و خدمات خودرو"
    }

]


def seed_business_categories(db: Session):

    for item in categories:

        exists = db.query(BusinessCategory).filter(
            BusinessCategory.slug == item["slug"]
        ).first()


        if not exists:

            category = BusinessCategory(**item)

            db.add(category)


    db.commit()