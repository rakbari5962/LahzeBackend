from app.database.database import SessionLocal

from app.models.booking import Booking
from app.models.opportunity import Opportunity



db = SessionLocal()



USER_ID = 3
OPPORTUNITY_ID = 1



print("SEED BOOKING RETRY DATA")
print("=======================")



opportunity = db.query(
    Opportunity
).filter(
    Opportunity.id == OPPORTUNITY_ID
).first()



if not opportunity:

    print(
        "Opportunity not found"
    )

    db.close()
    exit()



booking = Booking(

    user_id=USER_ID,

    business_id=opportunity.business_id,

    opportunity_id=opportunity.id,

    status="PENDING_CONFIRMATION"

)



db.add(booking)

db.commit()

db.refresh(booking)



print(
    "NEW BOOKING CREATED"
)

print(
    "-------------------"
)

print(
    "Booking ID:",
    booking.id
)

print(
    "User ID:",
    booking.user_id
)

print(
    "Business ID:",
    booking.business_id
)

print(
    "Opportunity ID:",
    booking.opportunity_id
)

print(
    "Status:",
    booking.status
)



db.close()