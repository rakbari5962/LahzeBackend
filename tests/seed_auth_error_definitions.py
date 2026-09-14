from app.database.database import SessionLocal

from app.models.error_definition import ErrorDefinition





def seed_auth_errors():


    print(
        "SEED AUTH ERROR DEFINITIONS"
    )

    print(
        "=========================="
    )


    db = SessionLocal()



    errors = [

        {
            "error_code": 201,
            "name": "OTP_NOT_FOUND",
            "description": "No OTP request found for this phone number",
            "severity": "MEDIUM"
        },

        {
            "error_code": 202,
            "name": "OTP_INVALID",
            "description": "Entered OTP code is invalid",
            "severity": "LOW"
        },

        {
            "error_code": 203,
            "name": "OTP_EXPIRED",
            "description": "OTP code has expired",
            "severity": "MEDIUM"
        },

        {
            "error_code": 204,
            "name": "OTP_ALREADY_USED",
            "description": "OTP code was already verified",
            "severity": "MEDIUM"
        },

        {
            "error_code": 205,
            "name": "OTP_COOLDOWN",
            "description": "User requested OTP too soon",
            "severity": "LOW"
        },

        {
            "error_code": 206,
            "name": "OTP_RATE_LIMIT",
            "description": "Too many OTP requests",
            "severity": "HIGH"
        }

    ]



    for item in errors:


        exists = (

            db.query(ErrorDefinition)

            .filter(

                ErrorDefinition.error_code == item["error_code"]

            )

            .first()

        )



        if not exists:


            error = ErrorDefinition(

                **item

            )


            db.add(error)


            print(

                "CREATED:",

                item["error_code"]

            )


        else:


            print(

                "EXISTS:",

                item["error_code"]

            )



    db.commit()



    db.close()



    print()

    print(
        "AUTH ERROR DEFINITIONS SEEDED ✅"
    )





if __name__ == "__main__":

    seed_auth_errors()