from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    """Task model"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    
    class Config:
        """Pydantic model configuration"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and fruits",
                "completed": False
            }
        }

# In-memory database for tasks
tasks: List[Task] = [] 