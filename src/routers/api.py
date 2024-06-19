from fastapi.routing import APIRouter

from src.core.config import settings
from src.routers.endpoints.task import task_router, tasks_router
from src.routers.endpoints.user import user_router

versioned_router = APIRouter()
versioned_router.include_router(tasks_router, prefix="/tasks", tags=["Task"])
versioned_router.include_router(task_router, prefix="/task", tags=["Task"])
versioned_router.include_router(user_router, prefix="/user", tags=["User"])

api_router = APIRouter()
api_router.include_router(versioned_router, prefix=f"/{settings.API_VERSION}")
