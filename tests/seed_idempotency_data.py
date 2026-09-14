from app.database.database import SessionLocal

from app.models.user import User
from app.models.business import Business



db = SessionLocal()



# -------------------------
# Create Test Users
# -------------------------

nazanin = User(
    phone_number="09120000010"
)


sara = User(
    phone_number="09120000011"
)



db.add(nazanin)
db.add(sara)

db.commit()


db.refresh(nazanin)
db.refresh(sara)



# -------------------------
# Create Test Business
# -------------------------

business = Business(
    owner_user_id=nazanin.id,
    name="Idempotency Test Salon",
    status="ACTIVE"
)


db.add(business)

db.commit()

db.refresh(business)



print("IDEMPOTENCY TEST DATA")
print("----------------------")

print(
    "Nazanin ID:",
    nazanin.id
)

print(
    "Sara ID:",
    sara.id
)

print(
    "Business ID:",
    business.id
)


db.close()