from app.database.database import SessionLocal

from app.services.review_ai_analysis_service import (
    analyze_business_reviews
)


db = SessionLocal()


result = analyze_business_reviews(
    db=db,
    business_id=11
)


print(result)


db.close()