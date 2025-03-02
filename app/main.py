"""
Main FastAPI application configuration
"""
from typing import Annotated
from fastapi import FastAPI

# Import routers
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router
from app.routers.auth  import router as auth_router

# Create FastAPI app
app = FastAPI(title="ToDo List API", redirect_slashes=True)

# Register routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(auth_router, prefix="/auth",   tags=["auth"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Welcome to the ToDo List API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

