import pytest
from passlib.hash import pbkdf2_sha256 as sha256

import src.core.error_msg as error_msg
from src.core.jwt_utils import decode_access_token
from src.models import User
from tests.utils.dummy_data import users
from tests.utils.util import get_versioned_endpoint

"""
Tested Routes

POST    /user/register
POST    /user/login
"""


"""
POST    /user/register
"""


def test_user_register_succeed(client, session):
    user_data = {"email": "new_user@mail.com", "password": "password"}
    response = client.post(get_versioned_endpoint("/user/register"), json=user_data)
    assert response.status_code == 200

    res_result = response.json().get("result")
    assert res_result.get("tokenType") == "bearer"

    last_db_user = session.query(User).order_by(User.id.desc()).first()
    assert decode_access_token(res_result.get("accessToken")).sub == last_db_user.id
    assert sha256.verify(user_data["password"], last_db_user.password)


def test_user_register_fail_duplicate_email(client):
    user_data = {"email": users[0].get("email"), "password": "password"}
    response = client.post(get_versioned_endpoint("/user/register"), json=user_data)

    assert response.status_code == 409


@pytest.mark.parametrize(
    "body",
    [
        {"email": "not_email", "password": "password"},
        {"email": "new_user@mail.com", "password": "short"},
    ],
)
def test_user_register_fail_invalid_body(client, body):
    response = client.post(get_versioned_endpoint("/user/register"), json=body)

    assert response.status_code == 422
    assert response.json()["error"]["message"] == error_msg.DATA_VALIDATION_FAIL


"""
POST /user/login
"""


def test_user_login_succeed(client):
    user = users[0]
    body = {"email": user.get("email"), "password": user.get("password")}

    response = client.post(get_versioned_endpoint("/user/login"), json=body)
    assert response.status_code == 200

    res_result = response.json().get("result")
    assert res_result.get("tokenType") == "bearer"
    assert decode_access_token(res_result.get("accessToken")).sub == user.get("id")


def test_user_login_fail_not_exist(client):
    body = {"email": "not_exist@mail.com", "password": "password"}

    response = client.post(get_versioned_endpoint("/user/login"), json=body)
    assert response.status_code == 404


def test_user_login_invalid_password(client):
    body = {"email": users[0].get("email"), "password": "wrong_password"}

    response = client.post(get_versioned_endpoint("/user/login"), json=body)
    assert response.status_code == 400
    assert response.json()["error"]["message"] == error_msg.INVALID_PASSWORD


@pytest.mark.parametrize(
    "body",
    [
        {"email": "not_email", "password": "password"},
        {"email": "new_user@mail.com", "password": "short"},
    ],
)
def test_user_login_fail_invalid_body(user_client, body):

    response = user_client.post(get_versioned_endpoint("/user/login"), json=body)
    assert response.status_code == 422
    assert response.json()["error"]["message"] == error_msg.DATA_VALIDATION_FAIL
