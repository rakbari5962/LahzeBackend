from app.database.database import SessionLocal

from app.services.review_ai_analysis_service import (
    analyze_business_reviews
)


db = SessionLocal()


result = analyze_business_reviews(
    db=db,
    business_id=1
)


print(result.id)
print(result.business_id)
print(result.total_reviews)
print(result.average_rating)
print(result.strengths)
print(result.weaknesses)
print(result.customer_sentiment)


db.close()