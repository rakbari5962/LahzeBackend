from fastapi.testclient import TestClient


from app.main import app


from app.database.database import SessionLocal


from app.models.error_occurrence import ErrorOccurrence

from app.models.error_definition import ErrorDefinition





client = TestClient(app)





def seed_errors():

    db = SessionLocal()


    definition = db.query(
        ErrorDefinition
    ).filter(
        ErrorDefinition.error_code == 500
    ).first()


    if not definition:

        definition = ErrorDefinition(

            error_code=500,

            name="SETTLEMENT_FAILED",

            description="Settlement failed",

            severity="CRITICAL"

        )

        db.add(definition)



    definition2 = db.query(
        ErrorDefinition
    ).filter(
        ErrorDefinition.error_code == 400
    ).first()


    if not definition2:

        definition2 = ErrorDefinition(

            error_code=400,

            name="PAYMENT_FAILED",

            description="Payment failed",

            severity="HIGH"

        )

        db.add(definition2)



    db.commit()



    errors = [

        ErrorOccurrence(

            error_code=500,

            device_info={

                "platform":"ANDROID",

                "device_model":"Galaxy A54",

                "app_version":"1.0.7"

            }

        ),


        ErrorOccurrence(

            error_code=500,

            device_info={

                "platform":"ANDROID",

                "device_model":"Galaxy A54",

                "app_version":"1.0.7"

            }

        ),


        ErrorOccurrence(

            error_code=400,

            device_info={

                "platform":"IOS",

                "device_model":"iPhone 15",

                "app_version":"1.0.8"

            }

        )

    ]


    db.add_all(errors)

    db.commit()


    db.close()







def test_error_analytics():


    print(
        "ERROR ANALYTICS TEST"
    )

    print(
        "===================="
    )


    seed_errors()



    response = client.get(

        "/admin/errors/analytics/",

        headers={

            "X-User-ID":"3"

        }

    )


    print()

    print(
        "DASHBOARD:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )


    assert response.status_code == 200



    response = client.get(

        "/admin/errors/analytics/top",

        headers={

            "X-User-ID":"3"

        }

    )


    print()

    print(
        "TOP ERRORS:"
    )

    print(
        response.json()
    )


    assert response.status_code == 200



    print()

    print(
        "ERROR ANALYTICS PASSED ✅"
    )





if __name__ == "__main__":

    test_error_analytics()