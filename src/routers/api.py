from fastapi.routing import APIRouter

from src.config import settings
from src.routers.router_task import task_router, tasks_router

versioned_router = APIRouter()
versioned_router.include_router(tasks_router, prefix="/tasks", tags=["Task"])
versioned_router.include_router(task_router, prefix="/task", tags=["Task"])


api_router = APIRouter()
api_router.include_router(versioned_router, prefix=f"/{settings.API_VERSION}")
