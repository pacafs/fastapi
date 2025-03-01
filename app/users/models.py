from passlib.context import CryptContext
from typing import Optional
from db.user import UserInDB, UserCreate, users_db

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
def get_user_by_username(username: str) -> Optional[UserInDB]:
    """
    Get a user by their username
    """
    for user in users_db:
        if user.username == username:
            return user
    return None

def get_user_by_email(email: str) -> Optional[UserInDB]:
    """
    Get a user by their email address
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
    """
    user = get_user_by_username(username)
    
    if not user:
        return None
        
    if not verify_password(password, user.hashed_password):
        return None
        
    return user

def create_user(user: UserCreate) -> UserInDB:
    """
    Create a new user in the database
    """
    user_id = len(users_db) + 1
    
    db_user = UserInDB(
        id=user_id,
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    
    users_db.append(db_user)
    
    return db_user