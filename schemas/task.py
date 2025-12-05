from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date
import uuid


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[date] = None

    @validator("due_date")
    def validate_due_date(cls, value):
        if value and value <= date.today():
            raise ValueError("due_date must be a future date")
        return value


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    due_date: Optional[date] = None


class Task(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    is_overdue: Optional[bool] = False
