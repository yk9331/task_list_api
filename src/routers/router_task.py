from fastapi import Depends, Response, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src import controllers, schemas
from src.core.utils import response_wrapper
from src.db.session import get_db, managed_transaction

tasks_router = APIRouter()
task_router = APIRouter()


@tasks_router.get("/", response_model=schemas.GenericListResponse[schemas.Task])
@response_wrapper
def get_task_list(
    db: Session = Depends(get_db),
):
    """
    Get task list
    """
    return controllers.task.get_all(db)


@task_router.post(
    "/",
    response_model=schemas.GenericSingleResponse[schemas.Task],
    status_code=status.HTTP_201_CREATED,
)
@response_wrapper
@managed_transaction
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Create new task
    """
    return controllers.task.create(db, obj_in=task_in)


@task_router.put("/{id}", response_model=schemas.GenericSingleResponse[schemas.Task])
@response_wrapper
@managed_transaction
def update_task(
    id: str,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    """
    Update task by id
    """
    return controllers.task.update_by_id(db, id=id, obj_in=task_in)


@task_router.delete("/{id}", response_class=Response)
@managed_transaction
def delete_task(
    id: str,
    db: Session = Depends(get_db),
):
    """
    Delete task by id
    """
    controllers.task.remove_by_id(db, id=id)
    return Response(status_code=status.HTTP_200_OK)
