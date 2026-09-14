from app.database.database import SessionLocal

from app.models.error_definition import ErrorDefinition



ERRORS = [

    {
        "error_code": 100,
        "name": "UNKNOWN_ERROR",
        "description": "خطای ناشناخته در سیستم رخ داده است.",
        "severity": "HIGH"
    },


    {
        "error_code": 200,
        "name": "AUTH_FAILED",
        "description": "احراز هویت کاربر ناموفق بود.",
        "severity": "MEDIUM"
    },


    {
        "error_code": 300,
        "name": "BOOKING_NOT_FOUND",
        "description": "رزرو مورد نظر پیدا نشد.",
        "severity": "MEDIUM"
    },


    {
        "error_code": 301,
        "name": "BOOKING_INVALID_STATUS",
        "description": "وضعیت فعلی رزرو اجازه انجام این عملیات را نمی‌دهد.",
        "severity": "MEDIUM"
    },


    {
        "error_code": 302,
        "name": "BOOKING_COMPLETE_FAILED",
        "description": "تکمیل رزرو با شکست مواجه شد.",
        "severity": "HIGH"
    },


    {
        "error_code": 400,
        "name": "PAYMENT_FAILED",
        "description": "پرداخت کاربر ناموفق بود.",
        "severity": "HIGH"
    },


    {
        "error_code": 500,
        "name": "SETTLEMENT_FAILED",
        "description": "فرآیند تسویه مالی انجام نشد.",
        "severity": "CRITICAL"
    },


    {
        "error_code": 501,
        "name": "SETTLEMENT_DUPLICATE",
        "description": "تلاش برای اجرای دوباره یک تسویه انجام شد.",
        "severity": "LOW"
    },


    {
        "error_code": 600,
        "name": "WALLET_OPERATION_FAILED",
        "description": "عملیات کیف پول ناموفق بود.",
        "severity": "HIGH"
    },


    {
        "error_code": 700,
        "name": "NETWORK_ERROR",
        "description": "ارتباط با سرور برقرار نشد.",
        "severity": "LOW"
    }

]



def seed_errors():

    db = SessionLocal()


    print("SEED ERROR DEFINITIONS")
    print("=====================")


    for error in ERRORS:


        existing = db.query(
            ErrorDefinition
        ).filter(
            ErrorDefinition.error_code ==
            error["error_code"]
        ).first()


        if existing:

            print(
                "EXISTS:",
                error["error_code"]
            )

            continue



        item = ErrorDefinition(
            **error
        )


        db.add(item)


        print(
            "CREATED:",
            error["error_code"],
            error["name"]
        )


    db.commit()

    db.close()


    print()
    print("ERROR DEFINITIONS SEEDED")



if __name__ == "__main__":

    seed_errors()