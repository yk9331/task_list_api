from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.schemas.base_model import CamelModel


class TokenPayload(CamelModel):
    token_type: str
    sub: str = Field(min_length=1, max_length=30)
    jti: UUID
    exp: datetime


class Token(CamelModel):
    access_token: str
    token_type: str = "bearer"
