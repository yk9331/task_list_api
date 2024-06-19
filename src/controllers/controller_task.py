from src.controllers.base_controller import BaseController
from src.models import Task
from src.schemas import TaskCreate, TaskUpdate


class TaskController(BaseController[Task, TaskCreate, TaskUpdate]):
    pass


task = TaskController(Task)
