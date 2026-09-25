from sqlalchemy.orm import Session


from app.repositories.review_attribute_repository import (
    get_or_create_attribute
)



def extract_attributes_from_text(
    text: str
):
    """
    Extract attributes from review text.

    Temporary rule-based extractor.
    Later this function will be replaced by LLM extraction.

    Output example:

    [
        {
            "key": "staff_behavior",
            "sentiment": "positive"
        },
        {
            "key": "price",
            "sentiment": "negative"
        }
    ]

    """


    results = []


    if (
        "برخورد" in text
        or "پرسنل" in text
        or "کارکنان" in text
    ):

        results.append(
            {
                "key": "staff_behavior",
                "sentiment": "positive"
            }
        )


    if (
        "تمیز" in text
        or "تمیزی" in text
        or "نظافت" in text
    ):

        results.append(
            {
                "key": "cleanliness",
                "sentiment": "positive"
            }
        )


    if (
        "قیمت" in text
        or "گران" in text
        or "بالا بود" in text
    ):

        results.append(
            {
                "key": "price",
                "sentiment": "negative"
            }
        )


    return results





def extract_review_attributes(
    db: Session,
    attributes: list
):
    """
    Converts extracted attribute keys
    into database attributes.

    Input example:

    [
        {
            "key": "staff_behavior",
            "sentiment": "positive"
        }
    ]

    """


    results = []


    for item in attributes:


        attribute = get_or_create_attribute(
            db=db,
            key=item["key"],
            label=item.get(
                "label",
                item["key"]
            )
        )


        results.append(
            {
                "attribute_id": attribute.id,

                "key": attribute.key,

                "label": attribute.label,

                "sentiment": item["sentiment"]
            }
        )


    return results