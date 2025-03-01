from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# =========================================
# Task Data Model
# =========================================

class TaskBase(BaseModel):
    """
    Base task model with common attributes
    """
    title: str
    description: Optional[str] = None
    completed: bool = False
    
    class Config:
        """Pydantic model configuration"""
        # Schema example for documentation
        json_schema_extra = {
            "example": {
                "title": "Complete project",
                "description": "Finish the FastAPI project by Friday",
                "completed": False
            }
        }

class TaskCreate(TaskBase):
    """
    Task create model
    """
    pass

class TaskUpdate(BaseModel):
    """
    Task update model
    
    All fields are optional to allow partial updates
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskInDB(TaskBase):
    """
    Task in database model
    """
    id: int
    created_at: datetime
    user_id: int  # Reference to the user who created the task

class TaskResponse(TaskInDB):
    """
    Task response model
    """
    pass

# =========================================
# In-memory Database
# =========================================
# This list serves as a simple in-memory database for tasks
# In a real application, this would be replaced with a proper database
tasks_db: List[TaskInDB] = []