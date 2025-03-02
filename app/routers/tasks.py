from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List
from db.task import Task
from db.database import pgSession
from app.models.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter()

# GET to /tasks from the prefix
@router.get("", response_model=List[Task], dependencies=None)
def get_tasks(session: pgSession):
    """Get all tasks"""
    return session.exec(select(Task)).all()

@router.get("/{task_id}", response_model=TaskResponse, dependencies=None)
def get_task(task_id: int, session: pgSession):
    """Get a specific task by ID"""
    task = session.get(Task, task_id)
    if task is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

# POST to /tasks from the prefix
@router.post("", response_model=TaskResponse, dependencies=None)
def create_task(task: TaskCreate, session: pgSession):
    """Create a new task"""
    # Convert TaskCreate to Task
    db_task = Task(**task.model_dump())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse, dependencies=None)
def update_task(task_id: int, updated_task: TaskUpdate, session: pgSession):
    """Update an existing task"""
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    for key, value in updated_task.model_dump().items():
        setattr(task, key, value)
        session.add(task)
        session.commit()
        session.refresh(task)
    return task


@router.delete("/{task_id}", response_model=TaskResponse, dependencies=None)
def delete_task(task_id: int, session: pgSession):
    """Delete a task"""
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")
    session.delete(task)
    session.commit()
    return task