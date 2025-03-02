from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from app.models.user import User, UserCreate, UserResponse, TokenResponse, LoginRequest
from db.database import pgSession
from app.auth.utils import hash_password, verify_password
from app.auth.jwt.jwt_handler import create_access_token
from app.auth.jwt.jwt_bearer import JWTBearer
from typing import List

# Create a router instance
router = APIRouter()
# Create a JWT bearer instance
jwt_bearer = JWTBearer()

@router.get('', response_model=List[UserResponse], dependencies=[Depends(jwt_bearer)])
def get_users(session: pgSession):
    """Get all users (without sensitive information)"""
    return session.exec(select(User)).all()

@router.get('/{user_id}', response_model=UserResponse, dependencies=[Depends(jwt_bearer)])
def get_user(user_id: int, session: pgSession):
    """Get a specific user by ID"""
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user

@router.post("/register", status_code=201, response_model=UserResponse, dependencies=None)
def create_user(user: UserCreate, session: pgSession):
    """Create a new user"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check if email already exists
    existing_email = session.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Hash the password
    hashed_password = hash_password(user.password)
    # Create the user
    db_user = User(**user.model_dump(), hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/login", status_code=200, response_model=TokenResponse, dependencies=None)
def login_user(login_data: LoginRequest, session: pgSession):
    """Login a user and return JWT token"""
    # Find the user in the database
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    
    # If user not found or password doesn't match
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    # Generate JWT token
    token = create_access_token(data={"sub": user.username, "user_id": user.id})
    return token
