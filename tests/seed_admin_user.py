from app.database.database import SessionLocal

from app.models.user import User





db = SessionLocal()



user = db.query(
    User
).filter(
    User.id == 3
).first()



if user:

    user.role = "ADMIN"

else:

    user = User(

        phone_number="09120000000",

        role="ADMIN"

    )

    db.add(user)



db.commit()

db.refresh(user)



print(
    "ADMIN USER READY"
)


print(
    "USER ID:",
    user.id
)


print(
    "ROLE:",
    user.role
)


db.close()