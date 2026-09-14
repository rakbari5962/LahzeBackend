from fastapi.testclient import TestClient


from app.main import app


from app.database.database import SessionLocal


from app.models.error_report import ErrorReport





client = TestClient(app)





def test_admin_error_api():


    print(
        "ADMIN ERROR API TEST"
    )

    print(
        "==================="
    )



    db = SessionLocal()



    report = db.query(
        ErrorReport
    ).order_by(
        ErrorReport.id.desc()
    ).first()



    if not report:

        print(
            "NO ERROR REPORT FOUND"
        )

        db.close()

        return



    report_id = report.id



    print()

    print(
        "USING REPORT ID:",
        report_id
    )



    db.close()





    # GET ALL REPORTS

    response = client.get(

        "/admin/errors/",

        headers={

            "X-User-ID": "3"

        }

    )



    print()

    print(
        "GET ALL ERRORS:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )







    # GET DETAILS


    response = client.get(

        f"/admin/errors/{report_id}",

        headers={

            "X-User-ID": "3"

        }

    )



    print()

    print(
        "GET ERROR DETAILS:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )








    # UPDATE STATUS


    response = client.patch(

        f"/admin/errors/{report_id}/status",

        params={

            "status": "INVESTIGATING"

        },

        headers={

            "X-User-ID": "3"

        }

    )



    print()

    print(
        "UPDATE STATUS:"
    )

    print(
        response.status_code
    )








    # ADD ADMIN NOTE


    response = client.patch(

        f"/admin/errors/{report_id}/note",

        params={

            "note":
            "مشکل در حال بررسی است."

        },

        headers={

            "X-User-ID": "3"

        }

    )



    print()

    print(
        "ADD NOTE:"
    )

    print(
        response.status_code
    )








    # VERIFY DATABASE


    db = SessionLocal()



    updated_report = db.query(

        ErrorReport

    ).filter(

        ErrorReport.id == report_id

    ).first()



    print()

    print(
        "DATABASE FINAL:"
    )


    print(

        {

            "id":
                updated_report.id,

            "status":
                updated_report.status,

            "admin_note":
                updated_report.admin_note

        }

    )



    db.close()





    assert updated_report.status == "INVESTIGATING"

    assert updated_report.admin_note is not None



    print()

    print(
        "ADMIN ERROR API PASSED ✅"
    )





if __name__ == "__main__":

    test_admin_error_api()