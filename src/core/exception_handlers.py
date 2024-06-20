from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import src.core.error_msg as error_msg


def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "error": {
                    "message": error_msg.DATA_VALIDATION_FAIL,
                    "details": exc.errors(),
                }
            }
        ),
    )


def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # TODO: Log error
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"message": exc.detail}},
        headers=getattr(exc, "headers", None),
    )


def default_exception_handler(request: Request, exc: Exception):
    # TODO: Log error
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": error_msg.INTERNAL_SERVER_ERROR_DEFAULT}},
    )
