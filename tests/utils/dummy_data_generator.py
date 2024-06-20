from src.models import Task
from tests.utils.dummy_data.task_data import tasks


def create_dummy_data(db):
    create_tasks(db)


def create_tasks(db):
    new_tasks = [Task(**task) for task in tasks]
    db.add_all(new_tasks)
    db.commit()
