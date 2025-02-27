from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# =========================================
# User Data Models
# =========================================

class UserBase(BaseModel):
    """
    Base user model with common attributes
    
    This model serves as the base for all user-related models
    and contains the common attributes shared across them.
    """
    email: str
    username: str


class UserCreate(UserBase):
    """
    User creation model
    
    This model extends the base user model and includes the
    password field needed when creating a new user.
    """
    password: str


class UserInDB(UserBase):
    """
    Database user model
    
    This model represents how users are stored in the database.
    It contains the hashed password instead of the plain text password,
    as well as additional database-specific fields.
    """
    id: int
    hashed_password: str
    disabled: bool = False
    created_at: datetime = datetime.now()
    
    class Config:
        """Pydantic model configuration"""
        # Allow model to be converted to/from ORM objects (useful when using SQLAlchemy)
        orm_mode = True


# =========================================
# In-memory Database
# =========================================
# This list serves as a simple in-memory database for users
# In a real application, this would be replaced with a proper database
users_db: List[UserInDB] = [] 