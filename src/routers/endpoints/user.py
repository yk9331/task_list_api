from fastapi.routing import APIRouter

from src import schemas
from src.core.auth import create_access_token
from src.core.decorators import response_wrapper

user_router = APIRouter()


@user_router.post("/login", response_model=schemas.GenericSingleResponse[schemas.Token])
@response_wrapper
def user_login(
    user: schemas.UserLogin,
):
    """
    Temporary login endpoint for user to get access token with name.
    """
    return schemas.Token(access_token=create_access_token(user.name))
