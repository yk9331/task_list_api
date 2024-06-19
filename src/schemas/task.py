from pydantic import ConfigDict, Field

from src.schemas.base_model import CamelModel


class TaskBase(CamelModel):
    name: str = Field(min_length=1, max_length=256)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    status: int = Field(description="0 = Incomplete, 1 = Complete", ge=0, le=1)


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: int
