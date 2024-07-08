import uuid
from datetime import datetime, timedelta, timezone

import jwt

import src.core.error_msg as error_msg
import src.core.exceptions as exc
from src.core.config import settings
from src.schemas import TokenPayload

algorithm = "HS256"


def create_access_token(user_id: str, expire_delta: timedelta = None) -> str:
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    data = {
        "token_type": "access_token",
        "sub": user_id,
        "jti": str(uuid.uuid4()),
        "exp": expire,
    }
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=algorithm)


def decode_access_token(token: str) -> TokenPayload:
    try:
        payload_dict = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[algorithm]
        )
        payload = TokenPayload(**payload_dict)
        return payload
    except Exception:
        raise exc.UnauthorizedError(error_msg.INVALID_TOKEN)
