from passlib.context import CryptContext
from pydantic import BaseModel
from db.user import UserBase, UserInDB, UserCreate, users_db
from typing import Optional


class UserResponse(UserBase):
    """
    User response model
    
    This model defines what user data is returned to clients.
    It excludes sensitive information like passwords.
    """
    id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com"
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
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "password123"
            }
        }

# Define token response model
class Token(BaseModel):
    access_token: str
    token_type: str



# =========================================
# Password Hashing Configuration
# =========================================
# CryptContext is from passlib and provides password hashing functionality
# bcrypt is a strong password hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The hashed password to verify against
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


# =========================================
# User Lookup Functions
# =========================================

def get_user_by_username(username: str) -> Optional[UserInDB]:
    """
    Get a user by their username
    
    Args:
        username (str): The username to look for
        
    Returns:
        Optional[UserInDB]: The user if found, None otherwise
    """
    for user in users_db:
        if user.username == username:
            return user
    return None


def get_user_by_email(email: str) -> Optional[UserInDB]:
    """
    Get a user by their email address
    
    Args:
        email (str): The email to look for
        
    Returns:
        Optional[UserInDB]: The user if found, None otherwise
    """
    for user in users_db:
        if user.email == email:
            return user
    return None


# =========================================
# User Authentication Functions
# =========================================

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate a user with username and password
    
    Args:
        username (str): The username to authenticate
        password (str): The plain text password to verify
        
    Returns:
        Optional[UserInDB]: The authenticated user if successful, None otherwise
    """
    # Get the user from the database
    user = get_user_by_username(username)
    
    # Check if user exists
    if not user:
        return None
        
    # Verify the password
    if not verify_password(password, user.hashed_password):
        return None
        
    return user


def create_user(user: UserCreate) -> UserInDB:
    """
    Create a new user in the database
    
    Args:
        user (UserCreate): The user data to create
        
    Returns:
        UserInDB: The created user with additional database fields
    """
    # Generate a new user ID (simple increment for in-memory DB)
    # In a real database, this would typically be handled automatically
    user_id = len(users_db) + 1
    
    # Create a new UserInDB instance with hashed password
    db_user = UserInDB(
        id=user_id,
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    
    # Add the user to the in-memory database
    users_db.append(db_user)
    
    return db_user