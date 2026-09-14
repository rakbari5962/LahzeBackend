from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from app.core.errors.exceptions import (
    LahzeException,
    SettlementException
)

from app.core.errors.error_codes import (
    ErrorCodes
)

from app.database.database import SessionLocal

from app.services.error_service import (
    record_error
)



app = FastAPI(
    title="Lahze API",
    description="Backend foundation for Lahze marketplace",
    version="0.1.0"
)





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

                "occurrence_id":
                    error_result["occurrence_id"]

            }

        }

    )





@app.get("/test-error")
def test_error():

    raise SettlementException(

        error_code=ErrorCodes.SETTLEMENT_FAILED,

        message="Settlement failed",

        context={

            "test": True,

            "reason": "MANUAL_TEST"

        }

    )





@app.get("/")
def root():

    return {

        "app": "Lahze",

        "message": "Lahze Backend is running",

        "version": "0.1.0"

    }





@app.get("/health")
def health_check():

    return {

        "status": "ok"

    }