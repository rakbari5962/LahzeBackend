from app.database.database import engine

from app.models.otp_request import OTPRequest


print(
    "CREATING OTP REQUEST TABLE"
)

print(
    "========================="
)


OTPRequest.__table__.create(

    bind=engine,

    checkfirst=True

)


print()

print(
    "OTP REQUEST TABLE CREATED ✅"
)