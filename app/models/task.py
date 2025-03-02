from pydantic import BaseModel
from typing import Optional

# Base model with common attributes
class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False
# Model for creating a new task (what clients send to your API)
class TaskCreate(TaskBase):
    # You might have additional validation here
    # For example, title must be at least 3 characters
    pass

# Model for updating an existing task
class TaskUpdate(BaseModel):
    # All fields are optional for updates
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Model for API responses (what your API sends back to clients)
class TaskResponse(TaskBase):
    id: int
    # You could add more fields that aren't in the database
    # For example, calculated fields or formatted dates
    
    # This tells Pydantic to use the orm_mode in V2
    model_config = {"from_attributes": True}