from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from src.models.tasks import Task, TaskCreate, TaskUpdate

def create_task(session: Session, task_in: TaskCreate, owner_id: int) -> Task:
    """Create a new task for a specific user using explicit assignment"""
    task_data = task_in.model_dump()
    db_task = Task(**task_data, owner_id=owner_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_tasks_by_user(session: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
    """Retrieve all tasks belonging to a specific user"""
    statement = select(Task).where(Task.owner_id == owner_id).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_task_by_id(session: Session, task_id: int, owner_id: int) -> Optional[Task]:
    """Retrieve a specific task by ID, ensuring ownership"""
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == owner_id)
    return session.exec(statement).first()

def update_task(session: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    """Update an existing task"""
    task_data = task_in.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, db_task: Task) -> None:
    """Delete a task"""
    session.delete(db_task)
    session.commit()
