from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from typing import List, Annotated
from db.database import pgSession
from app.models.task import Task, TaskCreate, TaskResponse, TaskUpdate
from app.utils.auth.jwt.jwt_bearer import JWTBearer

router = APIRouter()

# Create a JWT bearer instance
jwt_bearer = JWTBearer()
# Create a dependency to check the token
checkToken = Annotated[str, Depends(lambda: "test_token")] # jwt_bearer

# GET to /tasks from the prefix
@router.get("", response_model=List[Task])
def get_tasks(token: checkToken, session: pgSession):
    """Get all tasks"""
    return session.exec(select(Task)).all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, token: checkToken, session: pgSession):
    """Get a specific task by ID"""
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

# POST to /tasks from the prefix
@router.post("", response_model=TaskResponse)
def create_task(task: TaskCreate, token: checkToken, session: pgSession):
    """Create a new task"""
    # Convert TaskCreate to Task
    db_task = Task(**task.model_dump())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskUpdate, token: checkToken, session: pgSession):
    """Update an existing task"""
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    # Update task attributes from the request
    task_data = updated_task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, token: checkToken, session: pgSession):
    """Delete a task"""
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")
    session.delete(task)
    session.commit()
    return task