import os

from unittest.mock import patch, Mock


from app.services.sms_service import send_verification_code





def test_sms_service():


    print(
        "SMS SERVICE TEST"
    )

    print(
        "================"
    )



    os.environ["SMS_IR_API_KEY"] = "TEST_API_KEY"

    os.environ["SMS_IR_TEMPLATE_ID"] = "123456"





    mock_response = Mock()


    mock_response.json.return_value = {

        "status": 1,

        "message": "موفق",

        "data": {

            "messageId": 89545112,

            "cost": 1

        }

    }


    mock_response.raise_for_status.return_value = None





    with patch(

        "app.services.sms_service.requests.post",

        return_value=mock_response

    ) as mock_post:



        result = send_verification_code(

            mobile="09129367314",

            code="483921"

        )



        print()

        print(
            "SMS RESPONSE:"
        )

        print(
            result
        )





        mock_post.assert_called_once()



        request_args = mock_post.call_args





        print()

        print(
            "REQUEST URL:"
        )

        print(
            request_args[0][0]
        )





        print()

        print(
            "REQUEST HEADERS:"
        )

        print(
            request_args.kwargs["headers"]
        )





        print()

        print(
            "REQUEST BODY:"
        )

        print(
            request_args.kwargs["json"]
        )





        # URL CHECK

        assert (

            request_args[0][0]

            ==

            "https://api.sms.ir/v1/send/verify"

        )





        # HEADER CHECK

        assert (

            request_args.kwargs["headers"]["x-api-key"]

            ==

            "TEST_API_KEY"

        )


        assert (

            request_args.kwargs["headers"]["Content-Type"]

            ==

            "application/json"

        )


        assert (

            request_args.kwargs["headers"]["Accept"]

            ==

            "text/plain"

        )





        # BODY CHECK

        body = request_args.kwargs["json"]



        assert body["mobile"] == "09129367314"


        assert body["templateId"] == 123456


        assert body["parameters"][0]["name"] == "Code"


        assert body["parameters"][0]["value"] == "483921"





    print()

    print(
        "SMS SERVICE PASSED ✅"
    )





if __name__ == "__main__":

    test_sms_service()