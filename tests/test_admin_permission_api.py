from fastapi.testclient import TestClient


from app.main import app



client = TestClient(app)





def test_admin_permission():


    print(
        "ADMIN PERMISSION TEST"
    )

    print(
        "===================="
    )



    # بدون Header

    response = client.get(
        "/admin/errors/"
    )


    print()

    print(
        "WITHOUT HEADER:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 401






    # کاربر غیر ادمین

    response = client.get(

        "/admin/errors/",

        headers={

            "X-User-ID":"5"

        }

    )



    print()

    print(
        "CUSTOMER USER:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )



    assert response.status_code == 403






    # ادمین

    response = client.get(

        "/admin/errors/",

        headers={

            "X-User-ID":"3"

        }

    )



    print()

    print(
        "ADMIN USER:"
    )

    print(
        response.status_code
    )

    print(
        response.json()
    )


    assert response.status_code == 200



    print()

    print(
        "ADMIN PERMISSION PASSED ✅"
    )





if __name__ == "__main__":

    test_admin_permission()