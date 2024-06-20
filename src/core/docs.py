from src.schemas.response import ErrorResponse

doc_config = {
    "title": "Task List API",
    "version": "1.0.0",
    "servers": [{"url": "http://localhost:8000", "description": "Local server"}],
    "openapi_tags": [
        {"name": "Task", "description": "Task related operations"},
        {"name": "User", "description": "User authentication operations"},
    ],
    "responses": {
        400: {
            "description": "Client error",
            "model": ErrorResponse,
        },
        401: {
            "description": "Invalid authentication",
            "model": ErrorResponse,
        },
        403: {
            "description": "Permission denied",
            "model": ErrorResponse,
        },
        404: {
            "description": "Not found",
            "model": ErrorResponse,
        },
        422: {
            "description": "Data validation failed",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
    },
}
