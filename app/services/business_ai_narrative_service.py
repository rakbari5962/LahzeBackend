from sqlalchemy.orm import Session


from app.repositories.review_ai_analysis_repository import (
    get_business_analysis
)


from app.repositories.business_ai_narrative_repository import (
    create_or_update_narrative
)



MODEL_VERSION = "narrative-rule-v3"





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



    topic_sentiment = analysis.topic_sentiment or []



    positive_topics = []

    negative_topics = []



    for item in topic_sentiment:


        label = item.get(
            "label"
        )


        sentiment = item.get(
            "sentiment"
        )


        if sentiment == "positive":


            if label not in positive_topics:

                positive_topics.append(
                    label
                )



        elif sentiment == "negative":


            if label not in negative_topics:

                negative_topics.append(
                    label
                )





    summary_parts = []



    total_reviews = analysis.total_reviews



    if positive_topics:


        summary_parts.append(

            f"از بین {total_reviews} تجربه ثبت‌شده، "
            "مشتریان بیشترین رضایت را از "
            +
            " و ".join(positive_topics)
            +
            " داشته‌اند."

        )



    if negative_topics:


        summary_parts.append(

            "مهم‌ترین فرصت بهبود، "
            +
            " و ".join(negative_topics)
            +
            " است."

        )



    if not summary_parts:


        summary_parts.append(

            "بر اساس تجربه‌های ثبت شده، اطلاعات کافی برای تحلیل دقیق وجود ندارد."

        )



    summary = " ".join(summary_parts)





    positive_summary = None


    if positive_topics:


        positive_summary = (

            "نقاط قوت اصلی از نگاه مشتریان: "
            +
            "، ".join(positive_topics)

        )





    improvement_summary = None


    if negative_topics:


        improvement_summary = (

            "فرصت‌های بهبود: "
            +
            "، ".join(negative_topics)

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