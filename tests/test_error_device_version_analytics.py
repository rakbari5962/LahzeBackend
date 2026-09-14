from fastapi.testclient import TestClient


from app.main import app


from app.database.database import SessionLocal


from app.models.error_occurrence import ErrorOccurrence


from app.models.error_definition import ErrorDefinition





client = TestClient(app)





def seed_device_version_errors():


    db = SessionLocal()



    definition = db.query(
        ErrorDefinition
    ).filter(
        ErrorDefinition.error_code == 600
    ).first()



    if not definition:


        definition = ErrorDefinition(

            error_code=600,

            name="DEVICE_TEST_ERROR",

            description="Device analytics test error",

            severity="MEDIUM"

        )


        db.add(
            definition
        )


        db.commit()



    errors = [


        ErrorOccurrence(

            error_code=600,

            device_info={

                "platform":"ANDROID",

                "device_model":"Galaxy A54",

                "os_version":"Android 15",

                "app_version":"1.0.7"

            }

        ),



        ErrorOccurrence(

            error_code=600,

            device_info={

                "platform":"ANDROID",

                "device_model":"Galaxy A54",

                "os_version":"Android 15",

                "app_version":"1.0.7"

            }

        ),



        ErrorOccurrence(

            error_code=600,

            device_info={

                "platform":"IOS",

                "device_model":"iPhone 15",

                "os_version":"iOS 18",

                "app_version":"1.0.8"

            }

        )

    ]



    db.add_all(
        errors
    )


    db.commit()


    db.close()







def test_device_version_analytics():


    print(
        "DEVICE VERSION ANALYTICS TEST"
    )

    print(
        "============================="
    )



    seed_device_version_errors()



    # DEVICE ANALYTICS


    response = client.get(

        "/admin/errors/analytics/devices",

        headers={

            "X-User-ID":"3"

        }

    )



    print()

    print(
        "DEVICE ANALYTICS:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 200



    devices = response.json()



    galaxy = next(

        item for item in devices

        if item["device_model"] == "Galaxy A54"

    )



    assert galaxy["count"] >= 2





    # VERSION ANALYTICS


    response = client.get(

        "/admin/errors/analytics/versions",

        headers={

            "X-User-ID":"3"

        }

    )



    print()

    print(
        "VERSION ANALYTICS:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 200



    versions = response.json()



    version = next(

        item for item in versions

        if item["app_version"] == "1.0.7"

    )



    assert version["count"] >= 2




    print()

    print(
        "DEVICE VERSION ANALYTICS PASSED ✅"
    )





if __name__ == "__main__":

    test_device_version_analytics()