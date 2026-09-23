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


for review in reviews[:10]:

    print("\n====================")
    print("REVIEW:")
    print(review.comment)


    result = analyze_review_with_gemini(
        review.comment,
        review.rating
    )


    print("ANALYSIS:")
    print(result)


    results.append(result)



final = aggregate_review_ai_results(
    results
)


print("\n\nFINAL AGGREGATION")
print("====================")

print(final)