from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False




tasks = []