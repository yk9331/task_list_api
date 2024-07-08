from pydantic import SecretStr
from sqlalchemy.orm import Session

import src.core.error_msg as error_msg
import src.core.exceptions as exc
from src.controllers.base_controller import BaseController
from src.core.jwt_utils import create_access_token
from src.models import User
from src.schemas import UserCreate, UserLogin, UserRegister, UserToken, UserUpdate


class UserController(BaseController[User, UserCreate, UserUpdate]):
    def register(self, db: Session, *, user_in: UserRegister) -> UserToken:
        user_in.password = SecretStr(
            User.hash_password(user_in.password.get_secret_value())
        )
        user = self.create(db, obj_in=user_in)
        return UserToken(access_token=create_access_token(user.id))

    def login(self, db: Session, *, user_in: UserLogin) -> UserToken:
        user = self.get_by_filter_or_404(db, email=user_in.email)
        if not user.verify_password(user_in.password.get_secret_value()):
            raise exc.ClientError(error_msg.INVALID_PASSWORD)
        return UserToken(access_token=create_access_token(user.id))


user = UserController(User)
