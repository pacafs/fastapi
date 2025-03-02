"""
Main FastAPI application configuration
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import create_tables
# Import routers
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_tables()
    yield
    # Clean up resources on shutdown if needed
    pass

# Create FastAPI app
app = FastAPI(title="ToDo List API", redirect_slashes=True, lifespan=lifespan)


# Register routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Welcome to the ToDo List API",
        "documentation": "/docs",
        "version": "1.0.0"
    }




