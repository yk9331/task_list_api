from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src import controllers, schemas
from src.core.db.session import get_db, managed_transaction
from src.core.decorators import response_wrapper

user_router = APIRouter()


@user_router.post(
    "/register", response_model=schemas.GenericSingleResponse[schemas.UserToken]
)
@response_wrapper
@managed_transaction
def user_login(
    user_in: schemas.UserRegister,
    db: Session = Depends(get_db),
):
    """
    Temporary register endpoint for user to create account.
    """
    return controllers.user.register(db, user_in=user_in)


@user_router.post(
    "/login", response_model=schemas.GenericSingleResponse[schemas.UserToken]
)
@response_wrapper
def user_login(
    user_in: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    """
    Temporary login endpoint for user to login.
    """
    return controllers.user.login(db, user_in=user_in)
