from sqlalchemy.orm import Session

from app.models.review import Review

from app.repositories.review_ai_analysis_repository import (
    create_or_update_analysis
)


MODEL_VERSION = "rule-based-v3"



TOPIC_KEYWORDS = {

    "quality": [
        "کیفیت",
        "عالی",
        "خوب",
        "حرفه ای",
        "حرفه‌ای",
        "ماهر",
        "متخصص",
        "نتیجه",
        "رضایت"
    ],


    "staff_behavior": [
        "برخورد",
        "رفتار",
        "مودب",
        "محترم",
        "پرسنل",
        "کارکنان"
    ],


    "price": [
        "قیمت",
        "گران",
        "ارزان",
        "هزینه",
        "منصفانه"
    ],


    "waiting_time": [
        "انتظار",
        "معطل",
        "دیر",
        "تاخیر",
        "تأخیر",
        "زمان انتظار",
        "طول کشید"
    ],


    "cleanliness": [
        "تمیز",
        "تمیزی",
        "کثیف",
        "بهداشت",
        "نظافت"
    ],


    "equipment": [
        "تجهیزات",
        "دستگاه",
        "ابزار",
        "امکانات"
    ]

}



TOPIC_LABELS = {

    "quality": "کیفیت خدمات",

    "staff_behavior": "برخورد پرسنل",

    "price": "قیمت",

    "waiting_time": "زمان انتظار",

    "cleanliness": "نظافت و محیط",

    "equipment": "تجهیزات و امکانات"

}



POSITIVE_WORDS = [

    "عالی",
    "خوب",
    "بهترین",
    "رضایت",
    "راضی",
    "حرفه‌ای",
    "حرفه ای",
    "مودب",
    "محترم"

]



NEGATIVE_WORDS = [

    "بد",
    "ضعیف",
    "زیاد",
    "گران",
    "کثیف",
    "تاخیر",
    "تأخیر",
    "معطل",
    "زیاد بود",
    "کم بود"

]





def detect_topic_sentiment(
    comment,
    topic,
    keywords
):

    if not any(
        keyword in comment
        for keyword in keywords
    ):

        return None



    if topic == "waiting_time":

        if any(
            word in comment
            for word in [
                "زیاد",
                "طول کشید",
                "معطل",
                "تاخیر",
                "تأخیر",
                "کند"
            ]
        ):

            return "negative"



        if any(
            word in comment
            for word in [
                "سریع",
                "به موقع",
                "بدون انتظار"
            ]
        ):

            return "positive"



    if topic == "quality":

        if any(
            word in comment
            for word in [
                "عالی",
                "خوب",
                "حرفه‌ای",
                "حرفه ای",
                "ماهر",
                "متخصص",
                "رضایت"
            ]
        ):

            return "positive"



        if any(
            word in comment
            for word in [
                "ضعیف",
                "بد",
                "بی کیفیت",
                "نامناسب"
            ]
        ):

            return "negative"



    if topic == "staff_behavior":

        if any(
            word in comment
            for word in [
                "خوب",
                "مودب",
                "محترم",
                "عالی"
            ]
        ):

            return "positive"



        if any(
            word in comment
            for word in [
                "بد",
                "بی ادب",
                "نامحترم"
            ]
        ):

            return "negative"



    positive_score = 0

    negative_score = 0



    for word in POSITIVE_WORDS:

        if word in comment:

            positive_score += 1



    for word in NEGATIVE_WORDS:

        if word in comment:

            negative_score += 1



    if negative_score > positive_score:

        return "negative"



    elif positive_score > negative_score:

        return "positive"



    return "neutral"







def analyze_business_reviews(
    db: Session,
    business_id: int
):


    reviews = db.query(Review).filter(
        Review.business_id == business_id
    ).all()



    total_reviews = len(reviews)



    if total_reviews == 0:


        data = {

            "total_reviews": 0,

            "average_rating": None,

            "strengths": [],

            "weaknesses": [],

            "themes": [],

            "topic_sentiment": [],

            "customer_sentiment": {
                "positive": 0,
                "neutral": 0,
                "negative": 0
            },

            "model_version": MODEL_VERSION

        }


        return create_or_update_analysis(
            db,
            business_id,
            data
        )





    average_rating = sum(
        review.rating
        for review in reviews
    ) / total_reviews





    positive_count = 0

    neutral_count = 0

    negative_count = 0





    topic_stats = {}



    for topic in TOPIC_KEYWORDS:

        topic_stats[topic] = {

            "mentions": 0,

            "positive": 0,

            "negative": 0

        }





    for review in reviews:


        if review.rating >= 4:

            positive_count += 1


        elif review.rating == 3:

            neutral_count += 1


        else:

            negative_count += 1




        comment = (
            review.comment or ""
        ).lower()




        for topic, keywords in TOPIC_KEYWORDS.items():


            sentiment = detect_topic_sentiment(
                comment,
                topic,
                keywords
            )



            if sentiment:


                topic_stats[topic]["mentions"] += 1



                if sentiment == "positive":

                    topic_stats[topic]["positive"] += 1



                elif sentiment == "negative":

                    topic_stats[topic]["negative"] += 1







    strengths = []

    weaknesses = []

    themes = []

    topic_sentiment = []





    for topic, stats in topic_stats.items():


        if stats["mentions"] == 0:

            continue



        label = TOPIC_LABELS[topic]



        if stats["positive"] > stats["negative"]:

            sentiment = "positive"


        elif stats["negative"] > stats["positive"]:

            sentiment = "negative"


        else:

            sentiment = "neutral"


        topic_sentiment.append({

            "topic": topic,

            "label": label,

            "sentiment": sentiment,

            "mentions": stats["mentions"]

        })


        themes.append({

            "name": topic,

            "label": label,

            "mentions": stats["mentions"]

        })




        if sentiment == "positive":


            strengths.append({

                "name": topic,

                "label": label,

                "mentions": stats["mentions"],

                "positive_mentions": stats["positive"]

            })



        elif sentiment == "negative":


            weaknesses.append({

                "name": topic,

                "label": label,

                "mentions": stats["mentions"],

                "negative_mentions": stats["negative"]

            })







    customer_sentiment = {


        "positive": round(
            positive_count / total_reviews * 100,
            1
        ),


        "neutral": round(
            neutral_count / total_reviews * 100,
            1
        ),


        "negative": round(
            negative_count / total_reviews * 100,
            1
        )

    }





    data = {


        "total_reviews": total_reviews,


        "average_rating": str(
            round(
                average_rating,
                2
            )
        ),


        "strengths": strengths,


        "weaknesses": weaknesses,


        "themes": themes,


        "topic_sentiment": topic_sentiment,


        "customer_sentiment": customer_sentiment,


        "model_version": MODEL_VERSION

    }





    return create_or_update_analysis(

        db=db,

        business_id=business_id,

        data=data

    )