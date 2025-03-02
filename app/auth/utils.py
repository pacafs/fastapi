from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from app.auth.jwt.jwt_bearer import JWTBearer
from app.auth.jwt.jwt_handler import decode_token
from db.database import pgSession
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The hashed password to compare against
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

# Create a JWT bearer instance
jwt_bearer = JWTBearer()

# Import User model here to avoid circular imports
from app.models.user import User

def get_current_user(
    token: Annotated[str, Depends(jwt_bearer)], 
    session: Annotated[pgSession, Depends()]
) -> User:
    """
    Get the current authenticated user based on the JWT token
    
    Args:
        token (str): The JWT token
        session (Session): Database session
        
    Returns:
        User: The authenticated user object
        
    Raises:
        HTTPException: If the token is invalid or the user is not found
    """
    # Decode token to get user info
    payload = decode_token(token)
    
    # Check if token is valid
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    # Find the user in the database
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user