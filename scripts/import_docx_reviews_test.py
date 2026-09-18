import sys
import os


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from docx import Document


from app.database.database import SessionLocal


from app.models.booking import Booking
from app.models.review import Review


from app.services.review_ai_analysis_service import (
    analyze_business_reviews
)


from app.services.business_ai_narrative_service import (
    generate_business_narrative
)



DOCX_PATH = "comment-test.docx"


BUSINESS_ID = 11

USER_ID = 22

OPPORTUNITY_ID = 1



db = SessionLocal()



def extract_reviews(path):

    document = Document(path)

    comments = []


    for paragraph in document.paragraphs:

        text = paragraph.text.strip()


        if text:

            comments.append(text)


    return comments




comments = extract_reviews(
    DOCX_PATH
)



print(
    "Reviews found:",
    len(comments)
)



for comment in comments:


    booking = Booking(

        user_id=USER_ID,

        business_id=BUSINESS_ID,

        opportunity_id=OPPORTUNITY_ID,

        status="COMPLETED"

    )


    db.add(booking)

    db.commit()

    db.refresh(booking)



    review = Review(

        booking_id=booking.id,

        user_id=USER_ID,

        business_id=BUSINESS_ID,

        rating=5,

        comment=comment

    )


    db.add(review)



db.commit()



print(
    "Reviews imported successfully"
)



analysis = analyze_business_reviews(

    db=db,

    business_id=BUSINESS_ID

)



narrative = generate_business_narrative(

    db=db,

    business_id=BUSINESS_ID

)



print("\n========== AI ANALYSIS ==========")



print(
    "\nTotal reviews:",
    analysis.total_reviews
)



print(
    "\nStrengths:"
)

print(
    analysis.strengths
)



print(
    "\nWeaknesses:"
)

print(
    analysis.weaknesses
)



print(
    "\nTopic sentiment:"
)

print(
    analysis.topic_sentiment
)



print("\n========== NARRATIVE ==========")



print(
    narrative.summary
)


print(
    narrative.positive_summary
)


print(
    narrative.improvement_summary
)


print(
    "Trust:",
    narrative.trust_score
)