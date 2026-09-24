import time

from app.services.gemini_review_analysis_service import (
    analyze_review_with_gemini
)

from app.services.review_ai_llm_aggregation_service import (
    aggregate_review_ai_results
)

from app.services.attribute_extraction_service import (
    extract_attributes_from_text
)

from app.services.review_attribute_service import (
    process_review_attributes
)

from sqlalchemy.orm import Session

from app.models.review import Review

from app.repositories.review_ai_analysis_repository import (
    create_or_update_analysis
)


MODEL_VERSION = "llm-v1"


TOPIC_KEYWORDS = {

    "quality": [
        "کیفیت خدمات",
        "کیفیت کار",
        "کیفیت ارائه",
        "کیفیت ساخت",
        "کیفیت",
        "نتیجه کار",
        "نتیجه خدمات",
        "بی کیفیت",
        "بی‌کیفیت",
        "کیفیت پایین"
    ],

    "staff_behavior": [
        "برخورد پرسنل",
        "برخورد کارکنان",
        "برخورد",
        "رفتار پرسنل",
        "رفتار کارکنان",
        "پرسنل",
        "کارکنان",
        "مودب",
        "محترم",
        "محترمانه",
        "بی ادب",
        "بی‌ادب",
        "نامحترم"
    ],

    "price": [
        "قیمت خدمات",
        "قیمت",
        "گران",
        "ارزان",
        "هزینه",
        "منصفانه",
        "قیمت بالا",
        "قیمت زیاد",
        "قیمت مناسب",
        "هزینه بالا",
        "هزینه زیاد",
        "هزینه مناسب"
    ],

    "waiting_time": [
        "زمان انتظار",
        "انتظار",
        "معطل",
        "معطلی",
        "دیر",
        "تاخیر",
        "تأخیر",
        "طول کشید",
        "کند",
        "سریع",
        "به موقع",
        "بدون انتظار"
    ],

    "cleanliness": [
        "نظافت محیط",
        "محیط تمیز",
        "محیط کثیف",
        "تمیز",
        "تمیزی",
        "کثیف",
        "بهداشت",
        "نظافت"
    ],

    "equipment": [
        "تجهیزات",
        "دستگاه",
        "دستگاه‌ها",
        "ابزار",
        "امکانات",
        "تجهیزات مناسب",
        "تجهیزات خوب",
        "امکانات مناسب",
        "امکانات خوب"
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


TOPIC_POSITIVE_WORDS = {

    "quality": [
        "عالی",
        "خوب",
        "حرفه‌ای",
        "حرفه ای",
        "ماهر",
        "متخصص",
        "رضایت",
        "با کیفیت",
        "باکیفیت",
        "کیفیت بالا",
        "کیفیت عالی"
    ],

    "staff_behavior": [
        "خوب",
        "مودب",
        "محترم",
        "محترمانه",
        "عالی",
        "حرفه‌ای",
        "حرفه ای"
    ],

    "price": [
        "ارزان",
        "قیمت مناسب",
        "هزینه مناسب",
        "منصفانه",
        "ارزش خرید",
        "ارزشش رو داشت",
        "ارزش داشت"
    ],

    "waiting_time": [
        "سریع",
        "به موقع",
        "بدون انتظار",
        "معطلی نداشت",
        "سریع انجام شد"
    ],

    "cleanliness": [
        "تمیز",
        "تمیزی",
        "نظافت",
        "بهداشت",
        "پاکیزه"
    ],

    "equipment": [
        "مناسب",
        "خوب",
        "عالی",
        "کامل",
        "پیشرفته",
        "جدید",
        "به روز",
        "به‌روز"
    ]

}


TOPIC_NEGATIVE_WORDS = {

    "quality": [
        "ضعیف",
        "بد",
        "بی کیفیت",
        "بی‌کیفیت",
        "کیفیت پایین",
        "کیفیت بد",
        "نامناسب"
    ],

    "staff_behavior": [
        "بد",
        "بد بود",
        "بی ادب",
        "بی‌ادب",
        "نامحترم",
        "نامناسب",
        "محترمانه نبود",
        "خوب نبود",
        "راضی نبودم"
    ],

    "price": [
        "گران",
        "قیمت بالا",
        "قیمت زیاد",
        "هزینه بالا",
        "هزینه زیاد",
        "گران بود",
        "گران است",
        "صرفه نداشت"
    ],

    "waiting_time": [
        "زیاد",
        "طول کشید",
        "معطل",
        "معطلی",
        "تاخیر",
        "تأخیر",
        "کند",
        "دیر"
    ],

    "cleanliness": [
        "کثیف",
        "کثیف بود",
        "نظافت بد",
        "بهداشت ضعیف",
        "نامناسب"
    ],

    "equipment": [
        "ضعیف",
        "بد",
        "نامناسب",
        "کمبود",
        "خراب",
        "خراب بود",
        "قدیمی"
    ]

}


def split_into_sentences(comment):

    if not comment:
        return []

    normalized = comment.replace(
        "\r\n",
        "\n"
    )

    separators = [
        "؟",
        "?",
        "!",
        "؛",
        ";",
        ".",
        "\n"
    ]

    sentences = [normalized]

    for separator in separators:

        new_sentences = []

        for sentence in sentences:

            new_sentences.extend(
                sentence.split(separator)
            )

        sentences = new_sentences

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def sentence_has_topic(
    sentence,
    topic
):

    sentence_lower = sentence.lower()

    keywords = TOPIC_KEYWORDS[topic]

    return any(
        keyword.lower() in sentence_lower
        for keyword in keywords
    )


def detect_topic_sentiment(
    sentence,
    topic
):

    sentence_lower = sentence.lower()

    if not sentence_has_topic(
        sentence,
        topic
    ):
        return None


    negative_words = TOPIC_NEGATIVE_WORDS.get(
        topic,
        []
    )

    positive_words = TOPIC_POSITIVE_WORDS.get(
        topic,
        []
    )


    # Negative must always be checked first.
    # This prevents sentences such as:
    # "برخورد پرسنل خوب نبود"
    # from being classified as positive.

    if any(
        word in sentence_lower
        for word in negative_words
    ):

        return "negative"


    if any(
        word in sentence_lower
        for word in positive_words
    ):

        return "positive"


    return "neutral"


def is_valid_evidence(
    sentence,
    topic,
    sentiment
):

    """
    Evidence must contain a meaningful topic signal
    and a sentiment signal for that same topic.
    """

    if not sentence_has_topic(
        sentence,
        topic
    ):
        return False


    sentence_lower = sentence.lower()


    if sentiment == "negative":

        return any(
            word in sentence_lower
            for word in TOPIC_NEGATIVE_WORDS.get(
                topic,
                []
            )
        )


    if sentiment == "positive":

        return any(
            word in sentence_lower
            for word in TOPIC_POSITIVE_WORDS.get(
                topic,
                []
            )
        )


    return False


def analyze_business_reviews(
    db: Session,
    business_id: int
):

    start_time = time.time()

    print("AI ANALYSIS START")


    reviews = db.query(Review).filter(
        Review.business_id == business_id
    ).all()


    total_reviews = len(reviews)


    # فقط برای تست موقت LLM
    # بعد از اطمینان حذف می‌شود
    test_reviews = reviews[:5]


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



    llm_results = []

    positive_count = 0
    neutral_count = 0
    negative_count = 0



    for review in test_reviews:


        if review.rating >= 4:

            positive_count += 1


        elif review.rating == 3:

            neutral_count += 1


        else:

            negative_count += 1



        comment = review.comment or ""


        if not comment.strip():

            continue



        result = analyze_review_with_gemini(
            comment,
            review.rating
        )


        llm_results.append(result)

        review_attribute_list = []


        for item in result.get("topics", []):

            review_attribute_list.append(
                {
                    "key": item.get("topic"),
                    "label": item.get("label"),
                    "sentiment": item.get("sentiment")
                }
            )


        if review_attribute_list:

            process_review_attributes(
                db=db,
                business_id=business_id,
                attributes=review_attribute_list
            )



    print("LLM RESULTS COUNT:", len(llm_results))

    print("LLM RESULTS:")
    for r in llm_results:
        print(r)


    aggregated = aggregate_review_ai_results(
        llm_results
    )


    strengths = aggregated["strengths"]

    weaknesses = aggregated["weaknesses"]

    themes = aggregated["themes"]
    
    print(
        "THEMES RESULT:",
        themes
    )

    topic_sentiment = themes



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



    print(
        "TOTAL ANALYSIS TIME:",
        round(time.time() - start_time, 3),
        "seconds"
    )



    return create_or_update_analysis(
        db,
        business_id,
        data
    )