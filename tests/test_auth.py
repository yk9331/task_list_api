from datetime import timedelta

import jwt
from fastapi.security import HTTPAuthorizationCredentials

import src.core.error_msg as error_msg
import src.core.exceptions as exc
from src.core.auth import auth_user, create_access_token

"""
Tested Functions

src.core.auth.auth_user
"""


def test_user_auth_succeed():
    username = "user1"
    token = create_access_token(username)

    payload = auth_user(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    )

    assert payload.sub == username


def test_user_auth_fail_invalid_scheme():
    token = create_access_token("user1")

    try:
        auth_user(HTTPAuthorizationCredentials(scheme="Basic", credentials=token))
    except exc.UnauthorizedError as e:
        assert e.detail == error_msg.INVALID_AUTHORIZATION_SCHEME


def test_user_auth_fail_expired_token():
    token = create_access_token("user1", expire_delta=timedelta(seconds=-1))

    try:
        auth_user(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
    except exc.UnauthorizedError as e:
        assert e.detail == error_msg.INVALID_TOKEN


def test_user_auth_fail_invalid_token():
    invalid_token = jwt.encode(
        {
            "token_type": "access_token",
            "sub": "user1",
        },
        "invalid_key",
        algorithm="HS256",
    )

    try:
        auth_user(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_token)
        )
    except exc.UnauthorizedError as e:
        assert e.detail == error_msg.INVALID_TOKEN
