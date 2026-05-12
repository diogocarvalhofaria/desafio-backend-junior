from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    project_id: UUID

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskSummary(BaseModel):
    id: UUID
    title: str
    completed: bool
    project_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Task(TaskBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)