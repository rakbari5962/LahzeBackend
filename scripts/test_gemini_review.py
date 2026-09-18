from app.services.gemini_review_service import (
    generate_business_summary_with_gemini
)



analysis = {

    "total_reviews": 42,

    "strengths": [
        {
            "label": "کیفیت خدمات",
            "mentions": 25
        },
        {
            "label": "برخورد پرسنل",
            "mentions": 5
        }
    ],

    "weaknesses": [
        {
            "label": "زمان انتظار",
            "mentions": 5
        }
    ]

}



result = generate_business_summary_with_gemini(
    analysis
)


print("SUMMARY:")
print(result["summary"])

print("\nPOSITIVE:")
print(result["positive_summary"])

print("\nIMPROVEMENT:")
print(result["improvement_summary"])