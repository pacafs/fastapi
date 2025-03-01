from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .models import Task, tasks
from app.auth.jwt.jwt_bearer import JWTBearer


router = APIRouter()

# GET to /tasks from the prefix
@router.get("", response_model=List[Task], dependencies=[Depends(JWTBearer())])
async def get_tasks():
    """Get all tasks"""
    return tasks

@router.get("/{task_id}", response_model=Task, dependencies=[Depends(JWTBearer())])
async def get_task(task_id: int):
    """Get a specific task by ID"""
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found"
    )

# POST to /tasks from the prefix
@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def create_task(task: Task):
    """Create a new task"""
    tasks.append(task)
    return task

@router.put("/{task_id}", response_model=Task, dependencies=[Depends(JWTBearer())])
async def update_task(task_id: int, updated_task: Task):
    """Update an existing task"""
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found"
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())])
async def delete_task(task_id: int):
    """Delete a task"""
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found"
    )
