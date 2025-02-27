from pydantic import BaseModel
from typing import List, Optional

# =========================================
# Task Data Model
# =========================================

class Task(BaseModel):
    """
    Task model
    
    This model represents a task in the todo list application.
    Each task has an ID, title, optional description, and completion status.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    
    class Config:
        """Pydantic model configuration"""
        # Schema example for documentation
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and fruits",
                "completed": False
            }
        }


# =========================================
# In-memory Database
# =========================================
# This list serves as a simple in-memory database for tasks
# In a real application, this would be replaced with a proper database
tasks: List[Task] = []