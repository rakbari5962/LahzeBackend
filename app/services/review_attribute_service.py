from sqlalchemy.orm import Session


from app.services.attribute_matching_service import (
    match_attribute
)


from app.repositories.review_attribute_repository import (
    get_or_create_business_attribute_score,
    increase_positive_count,
    increase_negative_count
)





def process_review_attributes(
    db: Session,
    business_id: int,
    attributes: list
):


    results = []


    for item in attributes:

        print(
            "PROCESS ATTRIBUTE:",
            item
        )

        print(
            "MATCH INPUT:",
            item
        )
        
        attribute = match_attribute(
            db=db,
            attribute_key=item.get("key"),
            attribute_label=item.get("label")
        )
        print(
            "MATCH RESULT:",
            attribute.key if attribute else None
        )


        # اگر Attribute موجود نبود
        # فعلاً رد می‌کنیم
        # مرحله بعد می‌رود Admin Queue

        if not attribute:

            print(
                "UNKNOWN ATTRIBUTE:",
                item
            )

            continue




        score = get_or_create_business_attribute_score(
            db=db,
            business_id=business_id,
            attribute_id=attribute.id
        )



        if item["sentiment"] == "positive":


            increase_positive_count(
                db=db,
                score=score
            )



        elif item["sentiment"] == "negative":


            increase_negative_count(
                db=db,
                score=score
            )



        elif item["sentiment"] == "mixed":


            increase_positive_count(
                db=db,
                score=score
            )


            increase_negative_count(
                db=db,
                score=score
            )



        results.append(
            {
                "attribute_id": attribute.id,
                "label": attribute.label,
                "sentiment": item["sentiment"]
            }
        )


    return results