import pytest

from src.models import Task
from tests.utils.dummy_data import tasks
from tests.utils.util import get_versioned_endpoint

"""
Tested Routes

GET     /tasks
POST    /task
PUT     /task/<int:_id>
DELETE  /task/<int:_id>
"""


@pytest.mark.parametrize(
    "method, endpoint",
    [
        ("get", "/tasks"),
        ("post", "/task"),
        ("put", "/task/1"),
        ("delete", "/task/1"),
    ],
)
def test_anonymous_access_fail(client, method, endpoint):
    req_func = getattr(client, method)
    response = req_func(get_versioned_endpoint(endpoint))
    assert response.status_code == 401


"""
GET /tasks
"""


def test_user_get_tasks_succeed(user_client):
    response = user_client.get(get_versioned_endpoint("/tasks"))
    assert response.status_code == 200

    res_result = response.json().get("result")
    assert len(res_result) == len(tasks)
    assert all([a == b for a, b in zip(res_result, tasks)])


"""
POST /task
"""


def test_user_create_task_succeed(user_client, session):
    body = {"name": "new task"}

    response = user_client.post(get_versioned_endpoint("/task"), json=body)
    assert response.status_code == 201

    res_result = response.json().get("result")
    assert res_result["name"] == body["name"]
    assert res_result["status"] == 0

    last_db_task = session.query(Task).order_by(Task.id.desc()).first()
    assert last_db_task.name == body["name"]
    assert last_db_task.status == 0

    assert res_result["id"] == last_db_task.id


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"name": ""},
    ],
)
def test_user_create_task_fail_invalid_body(user_client, body):

    response = user_client.post(get_versioned_endpoint("/task"), json=body)
    assert response.status_code == 422


"""
PUT /task/<int:_id>
"""


def test_user_update_task_succeed(user_client, session):
    body = {"name": "updated task", "status": 1}
    task_id = 1

    response = user_client.put(get_versioned_endpoint(f"/task/{task_id}"), json=body)
    assert response.status_code == 200

    res_result = response.json().get("result")
    assert res_result["name"] == body["name"]
    assert res_result["status"] == body["status"]

    db_task = session.get(Task, task_id)
    assert db_task.name == body["name"]
    assert db_task.status == body["status"]


@pytest.mark.parametrize(
    "body",
    [
        {"name": "updated task"},
        {"status": 1},
        {"name": "updated task", "status": 3},
    ],
)
def test_user_update_task_fail_invalid_body(user_client, body):
    task_id = 1

    response = user_client.put(get_versioned_endpoint(f"/task/{task_id}"), json=body)
    assert response.status_code == 422


def test_user_update_task_fail_not_found(user_client):
    body = {"name": "updated task", "status": 1}
    task_id = 100

    response = user_client.put(get_versioned_endpoint(f"/task/{task_id}"), json=body)
    assert response.status_code == 404


"""
DELETE /task/<int:_id>
"""


def test_user_delete_task_succeed(user_client, session):
    task_id = 1

    response = user_client.delete(get_versioned_endpoint(f"/task/{task_id}"))
    assert response.status_code == 200

    db_task = session.get(Task, task_id)
    assert db_task is None


def test_user_delete_task_fail_not_found(user_client):
    task_id = 100

    response = user_client.delete(get_versioned_endpoint(f"/task/{task_id}"))
    assert response.status_code == 404
