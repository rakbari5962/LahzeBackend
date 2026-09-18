from app.services.gemini_review_analysis_service import (
    analyze_review_with_gemini
)


reviews = [

    "کیفیت خدمات عالی بود، برخورد پرسنل خوب بود ولی زمان انتظار کمی زیاد بود.",

    "کیفیت پایین بود و برخورد پرسنل مناسب نبود.",

    "قیمت بالاست ولی نسبت به چیزی که دریافت کردم ارزش دارد.",

    "محیط بسیار تمیز بود و امکانات خوبی داشت."

]


for index, review in enumerate(
    reviews,
    start=1
):

    print()
    print("=" * 60)
    print("REVIEW", index)
    print(review)
    print("-" * 60)


    try:

        result = analyze_review_with_gemini(
            review_text=review
        )


        print(
            result
        )


    except Exception as e:

        print(
            "ERROR:",
            e
        )