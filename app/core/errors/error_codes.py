class ErrorCodes:

    # General

    UNKNOWN_ERROR = 100



    # Authentication

    AUTH_FAILED = 200

    OTP_NOT_FOUND = 201

    OTP_INVALID = 202

    OTP_EXPIRED = 203

    OTP_ALREADY_USED = 204

    OTP_COOLDOWN = 205

    OTP_RATE_LIMIT = 206



    # Booking

    BOOKING_NOT_FOUND = 300

    BOOKING_INVALID_STATUS = 301

    BOOKING_COMPLETE_FAILED = 302




    # Payment

    PAYMENT_FAILED = 400

    PAYMENT_VERIFICATION_FAILED = 401




    # Settlement

    SETTLEMENT_FAILED = 500

    SETTLEMENT_DUPLICATE = 501




    # Wallet

    WALLET_OPERATION_FAILED = 600




    # Network / Client

    NETWORK_ERROR = 700




    # Business

    INVALID_BUSINESS_STATUS_TRANSITION = 800