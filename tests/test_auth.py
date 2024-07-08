from datetime import timedelta

import jwt
from fastapi.security import HTTPAuthorizationCredentials

import src.core.error_msg as error_msg
import src.core.exceptions as exc
from src.core.auth import auth_user
from src.core.jwt_utils import create_access_token

"""
Tested Functions

src.core.auth.auth_user
"""


def test_user_auth_succeed(session):
    user_id = 1
    token = create_access_token(user_id)

    user = auth_user(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=token), session
    )

    assert user.id == user_id


def test_user_auth_fail_not_exist(session):
    token = create_access_token(2)

    try:
        auth_user(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=token), session
        )
    except exc.UnauthorizedError as e:
        assert e.detail == error_msg.UNAUTHORIZED_DEFAULT


def test_user_auth_fail_invalid_scheme(session):
    token = create_access_token(1)

    try:
        auth_user(
            HTTPAuthorizationCredentials(scheme="Basic", credentials=token), session
        )
    except exc.UnauthorizedError as e:
        assert e.detail == error_msg.INVALID_AUTHORIZATION_SCHEME


def test_user_auth_fail_expired_token(session):
    token = create_access_token(1, expire_delta=timedelta(seconds=-1))

    try:
        auth_user(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=token), session
        )
    except exc.UnauthorizedError as e:
        assert e.detail == error_msg.INVALID_TOKEN


def test_user_auth_fail_invalid_token(session):
    invalid_token = jwt.encode(
        {
            "token_type": "access_token",
            "sub": 1,
        },
        "invalid_key",
        algorithm="HS256",
    )

    try:
        auth_user(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_token),
            session,
        )
    except exc.UnauthorizedError as e:
        assert e.detail == error_msg.INVALID_TOKEN
