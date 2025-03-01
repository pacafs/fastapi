from pydantic import BaseModel
from typing import List, Optional

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
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com"
            }
        }


class UserCreate(UserBase):
    """
    User creation model
    
    This model extends the base user model and includes the
    password field needed when creating a new user.
    """
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "password123"
            }
        }


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


class UserResponse(UserBase):
    """
    User response model
    
    This model defines what user data is returned to clients.
    It excludes sensitive information like passwords.
    """
    id: int


class LoginRequest(BaseModel):
    """
    JSON login request model
    
    This model defines the structure of the JSON login request.
    """
    username: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "password123"
            }
        }


class Token(BaseModel):
    """
    Token response model
    """
    access_token: str
    token_type: str


# =========================================
# In-memory Database
# =========================================
# This list serves as a simple in-memory database for users
# In a real application, this would be replaced with a proper database
users_db: List[UserInDB] = [] 