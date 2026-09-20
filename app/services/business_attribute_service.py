from sqlalchemy.orm import Session


from app.repositories.business_attribute_score_repository import (
    get_business_attribute_scores
)



MIN_ATTRIBUTE_MENTIONS = 2


MAX_DISPLAY_ATTRIBUTES = 5





def calculate_confidence(
    mentions: int
):

    if mentions >= 10:

        return "high"


    if mentions >= 5:

        return "medium"


    return "low"







def get_business_attribute_summary(
    db: Session,
    business_id: int
):


    rows = get_business_attribute_scores(
        db,
        business_id
    )



    attributes = []




    for score, attribute in rows:



        total = (

            score.positive_count

            +

            score.negative_count

        )



        if total < MIN_ATTRIBUTE_MENTIONS:

            continue





        positive_percentage = round(

            (
                score.positive_count

                /

                total

            )

            * 100,

            1

        )




        negative_percentage = round(

            (
                score.negative_count

                /

                total

            )

            * 100,

            1

        )






        item = {


            "label": attribute.label,


            "total_mentions": total,


            "positive_mentions":
                score.positive_count,


            "negative_mentions":
                score.negative_count,



            "positive_percentage":
                positive_percentage,



            "negative_percentage":
                negative_percentage,



            "confidence":
                calculate_confidence(total)

        }



        attributes.append(item)






    # مرتب سازی بر اساس تعداد تجربه

    attributes.sort(

        key=lambda x:
            x["total_mentions"],

        reverse=True

    )





    return {


        "attributes":
            attributes[:MAX_DISPLAY_ATTRIBUTES]

    }