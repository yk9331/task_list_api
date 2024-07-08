from datetime import datetime
from uuid import UUID

from src.schemas.base_model import CamelModel


class TokenPayload(CamelModel):
    token_type: str
    sub: int
    jti: UUID
    exp: datetime
