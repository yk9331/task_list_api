from typing import Generic, TypeVar

from pydantic import BaseModel

M = TypeVar("M")


class GenericSingleResponse(BaseModel, Generic[M]):
    result: M


class GenericListResponse(BaseModel, Generic[M]):
    result: list[M]
