from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import src.core.error_msg as error_msg
import src.core.exceptions as exc
from src import controllers
from src.core.db.session import get_db
from src.core.jwt_utils import decode_access_token

bearer = HTTPBearer(auto_error=False)


def auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    if credentials:
        if credentials.scheme.lower() != "bearer":
            raise exc.UnauthorizedError(error_msg.INVALID_AUTHORIZATION_SCHEME)
        payload = decode_access_token(credentials.credentials)
        user = controllers.user.get_by_id(db, id=payload.sub)
        if not user:
            raise exc.UnauthorizedError()
        return user
    else:
        raise exc.UnauthorizedError()
