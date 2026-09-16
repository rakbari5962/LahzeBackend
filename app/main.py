from app.routers.admin_release_error_router import router as admin_release_error_router

from app.routers.admin_release_router import router as admin_release_router

from app.routers.admin_treasury_router import router as admin_treasury_router

from app.routers.admin_dashboard_router import router as admin_dashboard_router

from app.routers.admin_reward_router import router as admin_reward_router

from app.services.scheduler_service import (
    start_scheduler
)

from app.api.routes.opportunity_expiration import router as opportunity_expiration_router

from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse



from app.core.errors.exceptions import (
    SettlementException,
    LahzeException
)


from app.core.errors.error_codes import ErrorCodes


from app.database.database import SessionLocal


from app.services.error_service import record_error





from app.api.routes.admin_errors import router as admin_errors_router

from app.api.routes.admin_error_analytics import router as admin_error_analytics_router

from app.api.routes.admin_device_analytics import router as admin_device_analytics_router

from app.api.routes.errors import router as errors_router

from app.api.routes.health import router as health_router

from app.api.routes.users import router as users_router

from app.api.routes.businesses import router as businesses_router

from app.api.routes.services import router as services_router

from app.api.routes.opportunities import router as opportunities_router

from app.api.routes.locations import router as locations_router

from app.api.routes.bookings import router as bookings_router

from app.api.routes.notifications import router as notifications_router

from app.api.routes.reviews import router as reviews_router

from app.api.routes.devices import router as devices_router

from app.api.routes.auth import router as auth_router

from app.api.routes.invitations import router as invitations_router

from app.api.routes.category_suggestions import router as category_suggestions_router

from app.api.routes.business_services import router as business_services_router

from app.api.routes.business_profile import router as business_profile_router

from app.api.routes.business_completion import router as business_completion_router

from app.api.routes.business_status import router as business_status_router

from app.api.routes.business_status_evaluator import router as business_status_evaluator_router

from app.api.routes.business_status_auto_update import router as business_status_auto_update_router

from app.api.routes.marketplace_opportunities import router as marketplace_opportunities_router

from app.api.routes.business_visibility import router as business_visibility_router





app = FastAPI( 

    title="Lahze Backend", 

    version="1.0.0",

    docs_url=None

)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():

    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css">

            <style>
                body {
                    background: #111827;
                }

                .swagger-ui {
                    filter: invert(0.9) hue-rotate(180deg);
                }

                .swagger-ui img {
                    filter: invert(1);
                }
            </style>
        </head>

        <body>

        <div id="swagger-ui"></div>

        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js"></script>

        <script>
            SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: '#swagger-ui'
            })
        </script>

        </body>
        </html>
        """
    )


@app.on_event("startup") 
def startup_event():

    start_scheduler()




@app.exception_handler(LahzeException)

async def lahze_exception_handler(

    request: Request,

    exc: LahzeException

):


    db = SessionLocal()


    try:


        error_result = record_error(

            db=db,

            error_code=exc.error_code,

            action=request.url.path,

            device_info={

                "platform": request.headers.get(
                    "X-Platform"
                ),

                "device_model": request.headers.get(
                    "X-Device-Model"
                ),

                "os_version": request.headers.get(
                    "X-OS-Version"
                ),

                "app_version": request.headers.get(
                    "X-App-Version"
                )

            },

            context={

                "method": request.method,

                "path": str(request.url.path),

                "details": exc.context

            }

        )


    finally:

        db.close()





    return JSONResponse(

        status_code=400,

        content={

            "success": False,

            "error": {

                "code": exc.error_code,

                "message": exc.message,

                "can_report": True,

                "occurrence_id": error_result["occurrence_id"]

            }

        }

    )









app.include_router(
    health_router
)


app.include_router(
    notifications_router
)

app.include_router(
    admin_reward_router
)


app.include_router(
    reviews_router
)


app.include_router(
    admin_release_router
)


app.include_router(
    admin_errors_router
)

app.include_router(
    admin_treasury_router
)

app.include_router(
    admin_release_error_router
)


app.include_router(
    admin_error_analytics_router
)

app.include_router(
    opportunity_expiration_router
)


app.include_router(
    admin_device_analytics_router
)

app.include_router(
    admin_dashboard_router
)

app.include_router(
    errors_router
)


app.include_router(
    devices_router
)


app.include_router(
    auth_router
)

app.include_router(
    invitations_router
)


app.include_router(
    users_router
)


app.include_router(
    businesses_router
)


app.include_router(
    category_suggestions_router
)





# مدیریت خدمات کسب و کار

app.include_router(
    business_services_router
)





# پروفایل کسب و کار

app.include_router(
    business_profile_router
)





# وضعیت تکمیل کسب و کار

app.include_router(
    business_completion_router
)





# مدیریت وضعیت کسب و کار

app.include_router(
    business_status_router
)





# ارزیابی وضعیت کسب و کار

app.include_router(
    business_status_evaluator_router
)





# بروزرسانی خودکار وضعیت کسب و کار

app.include_router(
    business_status_auto_update_router
)

app.include_router(
    marketplace_opportunities_router
)


# نمایش پذیری کسب و کار

app.include_router(
    business_visibility_router
)



app.include_router(
    services_router
)


app.include_router(
    opportunities_router
)


app.include_router(
    locations_router
)


app.include_router(
    bookings_router
)









@app.get("/test-error")

def test_error():


    raise SettlementException(

        error_code=ErrorCodes.SETTLEMENT_FAILED,

        message="Settlement failed",

        context={

            "test": True,

            "reason": "FULL_FLOW_TEST"

        }

    )









@app.get("/")

def root():


    return {

        "message": "Welcome to Lahze"

    }