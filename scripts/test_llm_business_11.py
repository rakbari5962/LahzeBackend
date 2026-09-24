from app.database.database import SessionLocal

from app.models.review import Review

from app.services.gemini_review_analysis_service import (
    analyze_review_with_gemini
)

from app.services.review_ai_llm_aggregation_service import (
    aggregate_review_ai_results
)



db = SessionLocal()


reviews = db.query(Review).filter(
    Review.business_id == 11
).all()



results = []


for review in reviews[:5]:

    print("\n====================")
    print("REVIEW:")
    print(review.comment)


    try:

        result = analyze_review_with_gemini(
            review.comment,
            review.rating
        )

    except Exception as e:

        print("FAILED:", e)

        continue


    print("\nAI RESULT:")
    print(result)


    results.append(result)



final = aggregate_review_ai_results(
    results
)


print("\n\n====================")
print("FINAL AGGREGATION")
print("====================")

print(final)