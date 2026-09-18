from sqlalchemy.orm import Session

from app.models.review_ai_analysis import ReviewAIAnalysis



def get_business_analysis(
    db: Session,
    business_id: int
):

    return db.query(
        ReviewAIAnalysis
    ).filter(
        ReviewAIAnalysis.business_id == business_id
    ).first()





def create_or_update_analysis(
    db: Session,
    business_id: int,
    data: dict
):

    analysis = get_business_analysis(
        db,
        business_id
    )



    if analysis:


        analysis.total_reviews = data["total_reviews"]

        analysis.average_rating = data["average_rating"]

        analysis.strengths = data["strengths"]

        analysis.weaknesses = data["weaknesses"]

        analysis.themes = data["themes"]

        analysis.topic_sentiment = data.get(
            "topic_sentiment",
            []
        )

        analysis.customer_sentiment = data["customer_sentiment"]

        analysis.model_version = data["model_version"]



    else:


        analysis = ReviewAIAnalysis(

            business_id=business_id,

            total_reviews=data["total_reviews"],

            average_rating=data["average_rating"],

            strengths=data["strengths"],

            weaknesses=data["weaknesses"],

            themes=data["themes"],

            topic_sentiment=data.get(
                "topic_sentiment",
                []
            ),

            customer_sentiment=data["customer_sentiment"],

            model_version=data["model_version"]

        )


        db.add(analysis)




    db.commit()

    db.refresh(analysis)


    return analysis







# دریافت تحلیل قابل نمایش برای مشتری

def get_public_business_analysis(
    db: Session,
    business_id: int
):

    return db.query(
        ReviewAIAnalysis
    ).filter(
        ReviewAIAnalysis.business_id == business_id
    ).first()