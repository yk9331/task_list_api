from pydantic import Field

from src.schemas.base_model import CamelModel


class UserLogin(CamelModel):
    name: str = Field(min_length=1, max_length=30)
