from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title : str = Field(..., min_length=1, max_length=255)
    description : str | None = Field(default=None, max_length=255)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title : str | None = None
    description : str | None = None
    completed : bool | None = None

class TaskResponse(TaskBase):
    id : int
    completed : bool
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)