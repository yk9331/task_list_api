from src.models import Task, User
from tests.utils.dummy_data import tasks, users


def create_dummy_data(db):
    create_users(db)
    create_tasks(db)


def create_tasks(db):
    new_tasks = [Task(**task) for task in tasks]
    db.add_all(new_tasks)
    db.commit()


def create_users(db):
    new_users = [User(**user) for user in users]
    for user in new_users:
        user.password = User.hash_password(user.password)
    db.add_all(new_users)
    db.commit()
