from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = None
    priority: str = Field(default="medium")  # low, medium, high
    status: str = Field(default="pending")   # pending, in_progress, completed
    due_date: Optional[datetime] = None

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign keys
    owner_id: int = Field(foreign_key="user.id", index=True)

    # Relationships
    owner: "User" = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

from src.models.user import User
