from sqlalchemy.orm import Session


from app.repositories.review_ai_analysis_repository import (
    get_business_analysis
)


from app.repositories.business_ai_narrative_repository import (
    create_or_update_narrative
)



MODEL_VERSION = "narrative-rule-v1"




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



    strengths = analysis.strengths or []

    weaknesses = analysis.weaknesses or []



    positive_items = [
        item["label"]
        for item in strengths
    ]


    negative_items = [
        item["label"]
        for item in weaknesses
    ]



    summary_parts = []



    if positive_items:

        summary_parts.append(

            "بیشترین رضایت مشتریان مربوط به "
            +
            " و ".join(positive_items)
            +
            " بوده است."

        )



    if negative_items:

        summary_parts.append(

            "مهم‌ترین موارد قابل بهبود "
            +
            " و ".join(negative_items)
            +
            " است."

        )



    if not summary_parts:

        summary_parts.append(

            "بر اساس تجربه‌های ثبت شده، اطلاعات کافی برای تحلیل دقیق وجود ندارد."

        )



    summary = " ".join(summary_parts)



    positive_summary = None

    if positive_items:

        positive_summary = (

            "نقاط قوت اصلی از نگاه مشتریان: "
            +
            "، ".join(positive_items)

        )



    improvement_summary = None

    if negative_items:

        improvement_summary = (

            "فرصت‌های بهبود: "
            +
            "، ".join(negative_items)

        )



    trust_score = calculate_trust_score(
        analysis.total_reviews,
        analysis.customer_sentiment
    )



    data = {

        "summary": summary,

        "positive_summary": positive_summary,

        "improvement_summary": improvement_summary,

        "trust_score": trust_score,

        "model_version": MODEL_VERSION

    }



    return create_or_update_narrative(

        db=db,

        business_id=business_id,

        data=data

    )





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