from sqlalchemy.orm import Session

from app.models.review_attribute import ReviewAttribute



ATTRIBUTE_ALIASES = {

    "staff_behavior": [
        "برخورد پرسنل",
        "رفتار کارکنان",
        "برخورد کارکنان",
        "رفتار پرسنل",
        "کارکنان",
        "پرسنل"
    ],


    "service_quality": [
        "کیفیت",
        "کیفیت خدمات",
        "کیفیت کار",
        "خدمات با کیفیت"
    ],


    "price_level": [
        "قیمت",
        "هزینه",
        "گران",
        "ارزان",
        "مبلغ"
    ],


    "value_for_money": [
        "ارزش خرید",
        "ارزش نسبت به قیمت",
        "به صرفه",
        "ارزش"
    ],


    "waiting_time": [
        "زمان انتظار",
        "معطلی",
        "تاخیر",
        "دیر"
    ],


    "cleanliness": [
        "نظافت",
        "تمیزی",
        "پاکیزگی",
        "محیط تمیز"
    ],


    "equipment_quality": [
        "تجهیزات",
        "امکانات",
        "دستگاه",
        "ابزار"
    ],


    "customer_care": [
        "پشتیبانی",
        "پاسخگویی",
        "رسیدگی"
    ],


    "delivery_speed": [
        "تحویل",
        "ارسال",
        "دریافت"
    ],


    "trustworthiness": [
        "اعتماد",
        "معتبر",
        "اطمینان"
    ]

}




def normalize_text(
    text: str
):

    if not text:
        return ""

    return (
        text
        .strip()
        .lower()
    )





def find_attribute_by_key(
    db: Session,
    key: str
):

    return (
        db.query(ReviewAttribute)
        .filter(
            ReviewAttribute.key == key
        )
        .first()
    )







def find_attribute_by_alias(
    db: Session,
    text: str
):

    text = normalize_text(text)


    for key, aliases in ATTRIBUTE_ALIASES.items():

        for alias in aliases:

            if normalize_text(alias) in text:

                attribute = find_attribute_by_key(
                    db=db,
                    key=key
                )


                if attribute:

                    return attribute


    return None








def find_attribute_by_label(
    db: Session,
    label: str
):

    if not label:
        return None


    return (
        db.query(ReviewAttribute)
        .filter(
            ReviewAttribute.label.ilike(
                f"%{label}%"
            )
        )
        .first()
    )










def match_attribute(
    db: Session,
    attribute_key: str = None,
    attribute_label: str = None
):


    # 1- Exact key

    if attribute_key:

        attribute = find_attribute_by_key(
            db=db,
            key=attribute_key
        )


        if attribute:

            return attribute





    # 2- Alias mapping

    if attribute_label:

        attribute = find_attribute_by_alias(
            db=db,
            text=attribute_label
        )


        if attribute:

            return attribute





    # 3- مستقیم با label

    if attribute_label:

        attribute = find_attribute_by_label(
            db=db,
            label=attribute_label
        )


        if attribute:

            return attribute





    return None