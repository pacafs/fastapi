from fastapi import FastAPI, HTTPException, Depends, status
from typing import List, Optional
from pydantic import BaseModel

# Models
from db.task import Task, tasks
from db.user import UserCreate, UserBase, UserInDB

# Authentication
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from auth.jwt_bearer import JWTBearer
from auth.users import authenticate_user, create_user, get_user_by_email
from datetime import timedelta

# =========================================
# API Setup
# =========================================

# Create FastAPI instance
app = FastAPI(
    title="ToDo List App",
    description="A simple REST API for todo list management with JWT authentication",
    version="1.0.0"
)

# =========================================
# Authentication Models
# =========================================

class Token(BaseModel):
    """
    Token response model
    
    This model defines the structure of the token response
    when a user successfully logs in.
    """
    access_token: str
    token_type: str
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class LoginRequest(BaseModel):
    """
    JSON login request model
    
    This model defines the structure of the JSON login request.
    It's used for the /login-json endpoint as an alternative to form data.
    """
    username: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "password123"
            }
        }

class UserResponse(UserBase):
    """
    User response model
    
    This model defines what user data is returned to clients.
    It excludes sensitive information like passwords.
    """
    id: int
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com"
            }
        }

# =========================================
# Authentication Routes
# =========================================

@app.post(
    "/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with username, email, and password"
)
def register_user(user: UserCreate):
    """
    User registration endpoint
    
    Creates a new user account with the provided information.
    Checks if the email is already registered to prevent duplicates.
    
    Args:
        user (UserCreate): User data including username, email, and password
        
    Returns:
        UserResponse: The created user without sensitive information
        
    Raises:
        HTTPException: If email is already registered
    """
    # Check if email already exists
    if get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = create_user(user)
    
    # Return user info (excluding password)
    return UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)


@app.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Login with username and password to get access token"
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User login endpoint
    
    Authenticates a user with username and password,
    and returns a JWT token on success.
    
    Args:
        form_data (OAuth2PasswordRequestForm): Username and password form data
        
    Returns:
        Token: JWT access token for authenticated requests
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    
    # Check if authentication failed
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with 30-minute expiration
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    # Return the token response
    return {"access_token": access_token["access_token"], "token_type": "bearer"}


@app.post(
    "/login-json",
    response_model=Token,
    summary="User login with JSON",
    description="Login with username and password (JSON format) to get access token"
)
def login_json(login_data: LoginRequest):
    """
    User login endpoint (JSON format)
    
    Authenticates a user with username and password from JSON body,
    and returns a JWT token on success.
    
    This is an alternative to the standard /login endpoint that uses form data.
    
    Args:
        login_data (LoginRequest): JSON with username and password
        
    Returns:
        Token: JWT access token for authenticated requests
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = authenticate_user(login_data.username, login_data.password)
    
    # Check if authentication failed
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with 30-minute expiration
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    # Return the token response
    return {"access_token": access_token["access_token"], "token_type": "bearer"}


# =========================================
# Todo List Routes
# =========================================

@app.get(
    "/tasks", 
    response_model=List[Task], 
    summary="List all tasks", 
    description="Returns a list of all tasks.",
    dependencies=[Depends(JWTBearer())]  # Protected route
)
def read_tasks():
    """
    Get all tasks
    
    Returns a list of all tasks in the system.
    Requires authentication.
    
    Returns:
        List[Task]: List of all tasks
    """
    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    summary="Get task by ID",
    dependencies=[Depends(JWTBearer())]  # Protected route
)
def read_task(task_id: int):
    """
    Get a specific task by ID
    
    Retrieves a task by its ID. Returns 404 if the task isn't found.
    Requires authentication.
    
    Args:
        task_id (int): The ID of the task to retrieve
        
    Returns:
        Task: The requested task
        
    Raises:
        HTTPException: If task not found
    """
    for task in tasks:
        if task.id == task_id:
            return task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Task not found"
    )


@app.post(
    "/tasks", 
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a new task with the provided information",
    dependencies=[Depends(JWTBearer())]  # Protected route
)
def create_task(task: Task):
    """
    Create a new task
    
    Creates a new task with the provided information.
    Requires authentication.
    
    Args:
        task (Task): The task data to create
        
    Returns:
        Task: The created task
    """
    tasks.append(task)
    return task


@app.put(
    "/tasks/{task_id}", 
    response_model=Task,
    summary="Update a task",
    description="Updates an existing task with new information",
    dependencies=[Depends(JWTBearer())]  # Protected route
)
def update_task(task_id: int, updated_task: Task):
    """
    Update an existing task
    
    Updates a task with the provided information.
    Returns 404 if the task isn't found.
    Requires authentication.
    
    Args:
        task_id (int): The ID of the task to update
        updated_task (Task): The new task data
        
    Returns:
        Task: The updated task
        
    Raises:
        HTTPException: If task not found
    """
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            # Update the existing task with the new values
            tasks[idx].title = updated_task.title
            tasks[idx].description = updated_task.description
            tasks[idx].completed = updated_task.completed
            return tasks[idx]  # Return the updated task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )


@app.delete(
    "/tasks/{task_id}", 
    response_model=Task,
    summary="Delete a task",
    description="Deletes a task by ID",
    dependencies=[Depends(JWTBearer())]  # Protected route
)
def delete_task(task_id: int):
    """
    Delete a task
    
    Deletes a task by its ID.
    Returns 404 if the task isn't found.
    Requires authentication.
    
    Args:
        task_id (int): The ID of the task to delete
        
    Returns:
        Task: The deleted task
        
    Raises:
        HTTPException: If task not found
    """
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(idx)
            return deleted_task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )


# =========================================
# API Entry Point
# =========================================

if __name__ == "__main__":
    import uvicorn
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get server configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    # Start the server
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        reload=debug
    )