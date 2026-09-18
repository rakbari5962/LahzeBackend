from sqlalchemy.orm import Session


from app.repositories.review_ai_analysis_repository import (
    get_business_analysis
)


from app.repositories.business_ai_narrative_repository import (
    create_or_update_narrative
)


from app.services.gemini_review_service import (
    generate_business_summary_with_gemini
)





def generate_business_narrative(
    db: Session,
    business_id: int
):


    analysis = get_business_analysis(
        db,
        business_id
    )


    if not analysis:

        return None



    analysis_payload = {

    "strengths": [
        {
            "topic": item.get("name"),
            "label": item.get("label"),
            "mentions": item.get("mentions"),
            "positive_mentions": item.get("positive_mentions")
        }
        for item in (analysis.strengths or [])
    ],

    "weaknesses": [
        {
            "topic": item.get("name"),
            "label": item.get("label"),
            "mentions": item.get("mentions"),
            "negative_mentions": item.get("negative_mentions")
        }
        for item in (analysis.weaknesses or [])
    ]

    }



    try:

        narrative_result = generate_business_summary_with_gemini(
            analysis_payload
        )

        model_version = "gemini-narrative-v1"



    except Exception:

        narrative_result = generate_rule_based_summary(
            analysis
        )

        model_version = "rule-based-fallback-v1"





    trust_score = calculate_trust_score(

        analysis.total_reviews,

        analysis.customer_sentiment

    )





    data = {

        "summary": narrative_result.get(
            "summary"
        ),


        "positive_summary": narrative_result.get(
            "positive_summary"
        ),


        "improvement_summary": narrative_result.get(
            "improvement_summary"
        ),


        "trust_score": trust_score,


        "model_version": model_version

    }





    return create_or_update_narrative(

        db=db,

        business_id=business_id,

        data=data

    )









def generate_rule_based_summary(
    analysis
):


    strengths = [

        item.get("label")

        for item in (analysis.strengths or [])

        if isinstance(item, dict)

    ]


    weaknesses = [

        item.get("label")

        for item in (analysis.weaknesses or [])

        if isinstance(item, dict)

    ]



    summary_parts = []



    if strengths:

        summary_parts.append(

            "بر اساس بازخوردهای ثبت‌شده، "

            "این مجموعه در زمینه "

            +

            " و ".join(strengths)

            +

            " بازخوردهای مثبتی دریافت کرده است."

        )



    if weaknesses:

        summary_parts.append(

            "بهبود "

            +

            " و ".join(weaknesses)

            +

            " می‌تواند به ارتقای تجربه مشتری کمک کند."

        )



    if not summary_parts:

        summary_parts.append(

            "بر اساس بازخوردهای ثبت‌شده، اطلاعات کافی برای تحلیل دقیق وجود ندارد."

        )



    return {


        "summary": " ".join(summary_parts),


        "positive_summary": (

            "نقاط قوت اصلی: "

            +

            "، ".join(strengths)

        ) if strengths else None,



        "improvement_summary": (

            "فرصت‌های بهبود: "

            +

            "، ".join(weaknesses)

        ) if weaknesses else None

    }









def calculate_trust_score(

    total_reviews: int,

    sentiment: dict

):


    if total_reviews == 0:

        return 0



    positive = sentiment.get(

        "positive",

        0

    )



    review_factor = min(

        total_reviews * 5,

        50

    )



    sentiment_factor = positive / 2



    score = int(

        review_factor +

        sentiment_factor

    )



    return min(

        score,

        100

    )