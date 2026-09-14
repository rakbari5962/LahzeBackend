import requests
import os

from dotenv import load_dotenv


load_dotenv()


SMS_IR_VERIFY_URL = "https://api.sms.ir/v1/send/verify"

SMS_IR_TEMPLATE_URL = "https://api.sms.ir/v1/send/verify"


def send_verification_code(
    mobile: str,
    code: str
):

    api_key = os.getenv(
        "SMS_IR_API_KEY"
    )

    template_id = os.getenv(
        "SMS_IR_TEMPLATE_ID"
    )


    # Development mode

    if not api_key or not template_id:

        print(
            f"[DEV SMS] {mobile} -> OTP: {code}"
        )

        return {

            "status": "development",

            "mobile": mobile,

            "code": code

        }


    headers = {

        "x-api-key": api_key,

        "Content-Type": "application/json",

        "Accept": "text/plain"

    }


    payload = {

        "mobile": mobile,

        "templateId": int(template_id),

        "parameters": [

            {

                "name": "Code",

                "value": code

            }

        ]

    }


    response = requests.post(

        SMS_IR_VERIFY_URL,

        json=payload,

        headers=headers

    )


    print(
        "OTP SMS STATUS:",
        response.status_code
    )


    print(
        "OTP SMS BODY:",
        response.text
    )


    response.raise_for_status()


    return response.json()





def send_booking_notification(
    mobile: str,
    business_name: str,
    booking_id: int
):

    api_key = os.getenv(
        "SMS_IR_API_KEY"
    )

    template_id = os.getenv(
        "SMS_IR_BOOKING_TEMPLATE_ID"
    )


    # Development mode

    if not api_key or not template_id:

        print(
            f"[DEV SMS] New booking notification -> "
            f"{mobile} | Business: {business_name} | "
            f"Booking ID: {booking_id}"
        )

        return {

            "status": "development",

            "mobile": mobile,

            "business_name": business_name,

            "booking_id": booking_id

        }



    headers = {

        "x-api-key": api_key,

        "Content-Type": "application/json",

        "Accept": "text/plain"

    }



    payload = {

        "mobile": mobile,

        "templateId": int(template_id),

        "parameters": [

            {

                "name": "BusinessName",

                "value": business_name

            },

            {

                "name": "BookingId",

                "value": str(booking_id)

            }

        ]

    }



    response = requests.post(

        SMS_IR_TEMPLATE_URL,

        json=payload,

        headers=headers

    )


    print(
        "BOOKING SMS STATUS:",
        response.status_code
    )


    print(
        "BOOKING SMS BODY:",
        response.text
    )


    response.raise_for_status()


    return response.json()





def send_booking_confirmation_notification(
    mobile: str,
    business_name: str,
    booking_id: int
):

    api_key = os.getenv(
        "SMS_IR_API_KEY"
    )

    template_id = os.getenv(
        "SMS_IR_BOOKING_CONFIRM_TEMPLATE_ID"
    )


    # Development mode

    if not api_key or not template_id:

        print(
            f"[DEV SMS] Booking confirmed -> "
            f"{mobile} | Business: {business_name} | "
            f"Booking ID: {booking_id}"
        )

        return {

            "status": "development",

            "mobile": mobile,

            "business_name": business_name,

            "booking_id": booking_id

        }



    headers = {

        "x-api-key": api_key,

        "Content-Type": "application/json",

        "Accept": "text/plain"

    }



    payload = {

        "mobile": mobile,

        "templateId": int(template_id),

        "parameters": [

            {

                "name": "BusinessName",

                "value": business_name

            },

            {

                "name": "BookingId",

                "value": str(booking_id)

            }

        ]

    }



    response = requests.post(

        SMS_IR_TEMPLATE_URL,

        json=payload,

        headers=headers

    )


    print(
        "BOOKING CONFIRM SMS STATUS:",
        response.status_code
    )


    print(
        "BOOKING CONFIRM SMS BODY:",
        response.text
    )


    response.raise_for_status()

def send_booking_cancellation_notification(
    mobile: str,
    business_name: str,
    booking_id: int,
    penalty_amount: int
):

    api_key = os.getenv(
        "SMS_IR_API_KEY"
    )


    template_id = os.getenv(
        "SMS_IR_BOOKING_CANCEL_TEMPLATE_ID"
    )


    if not api_key or not template_id:

        print(
            f"[DEV SMS] Booking cancelled -> "
            f"{mobile} | Business: {business_name} | "
            f"Booking ID: {booking_id} | "
            f"Penalty: {penalty_amount}"
        )


        return {

            "status": "development",

            "mobile": mobile,

            "business_name": business_name,

            "booking_id": booking_id,

            "penalty_amount": penalty_amount

        }



    headers = {

        "x-api-key": api_key,

        "Content-Type": "application/json",

        "Accept": "text/plain"

    }



    payload = {

        "mobile": mobile,

        "templateId": int(template_id),

        "parameters": [

            {
                "name": "BusinessName",
                "value": business_name
            },

            {
                "name": "BookingId",
                "value": str(booking_id)
            },

            {
                "name": "PenaltyAmount",
                "value": str(penalty_amount)
            }

        ]

    }



    response = requests.post(

        SMS_IR_TEMPLATE_URL,

        json=payload,

        headers=headers

    )


    print(
        "BOOKING CANCEL SMS STATUS:",
        response.status_code
    )


    print(
        "BOOKING CANCEL SMS BODY:",
        response.text
    )


    response.raise_for_status()


    return response.json()
