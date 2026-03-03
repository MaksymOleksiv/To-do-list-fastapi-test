import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.core.config import StatusEnum


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: StatusEnum | None = StatusEnum.pending
    due_date: datetime.datetime | None = Field(None, description="Due date in ISO 8601 format (e.g., '2024-12-31T23:59:59')", example="2024-12-31T23:59:59")

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TaskHistoryResponse(BaseModel):
    id: int
    task_id: int
    field: str
    old_value: str | None
    new_value: str | None
    changed_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseModel):
    status: str = "Ok"
