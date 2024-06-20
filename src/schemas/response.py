from typing import Any, Generic, TypeVar

from pydantic import BaseModel

M = TypeVar("M")


class GenericSingleResponse(BaseModel, Generic[M]):
    result: M


class GenericListResponse(BaseModel, Generic[M]):
    result: list[M]


class ErrorInfo(BaseModel):
    message: str
    details: Any = None


class ErrorResponse(BaseModel):
    error: ErrorInfo
