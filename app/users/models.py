from passlib.context import CryptContext
from typing import Optional
from app.models.user import User, UserCreate

# =========================================
# Password Hashing Configuration
# =========================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    """
    return pwd_context.hash(password)

# =========================================
# User Lookup Functions
# =========================================
def get_user_by_username(username: str) -> Optional[User]:
    """
    Get a user by their username
    """

def get_user_by_email(email: str) -> Optional[User]:
    """
    Get a user by their email address
    """


# =========================================
# User Authentication Functions
# =========================================
def authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticate a user with username and password
    """
    user = get_user_by_username(username)
    
    if not user:
        return None
        
    if not verify_password(password, user.hashed_password):
        return None
        
    return user

