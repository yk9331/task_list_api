from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

import src.core.exception_handlers as exception_handlers
from src.core.docs import doc_config
from src.routers.api import api_router

app = FastAPI(**doc_config)

app.add_exception_handler(
    RequestValidationError,
    exception_handlers.validation_exception_handler,
)
app.add_exception_handler(
    ValidationError,
    exception_handlers.validation_exception_handler,
)
app.add_exception_handler(
    StarletteHTTPException,
    exception_handlers.http_exception_handler,
)
app.add_exception_handler(
    Exception,
    exception_handlers.default_exception_handler,
)

app.include_router(api_router)
