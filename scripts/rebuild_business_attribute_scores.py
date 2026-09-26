from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.review_ai_result import ReviewAIResult

from app.services.review_attribute_service import (
    process_review_attributes
)

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


BUSINESS_ID = 1



def rebuild_business_attribute_scores(
    db: Session,
    business_id: int
):

    results = db.query(
        ReviewAIResult
    ).filter(
        ReviewAIResult.business_id == business_id
    ).all()


    print(
        "FOUND AI RESULTS:",
        len(results)
    )


    for result in results:

        print(
            "PROCESS REVIEW:",
            result.review_id
        )


        attributes = []


        for item in result.topics:


            attributes.append(
                {
                    "key": item.get("topic"),
                    "label": item.get("label"),
                    "sentiment": item.get("sentiment")
                }
            )


        if attributes:

            print(
                "ATTRIBUTES:",
                attributes
            )


            process_review_attributes(
                db=db,
                business_id=business_id,
                attributes=attributes
            )


    print(
        "REBUILD COMPLETED"
    )



if __name__ == "__main__":


    db = SessionLocal()


    try:

        rebuild_business_attribute_scores(
            db=db,
            business_id=BUSINESS_ID
        )


    finally:

        db.close()