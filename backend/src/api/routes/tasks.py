from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.config import get_session
from src.models.tasks import TaskRead, TaskCreate, TaskUpdate
from src.services import tasks as task_service
from src.api.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
def read_tasks(
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Retrieve all tasks for the current user"""
    return task_service.get_tasks_by_user(session, current_user_id, skip, limit)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
    task_in: TaskCreate
):
    """Create a new task for the current user"""
    return task_service.create_task(session, task_in, current_user_id)

@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    *,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
    task_id: int
):
    """Retrieve a specific task for the current user"""
    task = task_service.get_task_by_id(session, task_id, current_user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    *,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
    task_id: int,
    task_in: TaskUpdate
):
    """Update a specific task for the current user"""
    task = task_service.get_task_by_id(session, task_id, current_user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_service.update_task(session, task, task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    *,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
    task_id: int
):
    """Delete a specific task for the current user"""
    task = task_service.get_task_by_id(session, task_id, current_user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_service.delete_task(session, task)
    return None
