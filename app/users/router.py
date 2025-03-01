from fastapi import APIRouter, Depends, HTTPException, status
from db.user import UserCreate, users_db
from app.auth.jwt.jwt_bearer import JWTBearer
from app.users.models import get_user_by_username, authenticate_user, create_user

router = APIRouter()

@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_users():
    """Get all users (without sensitive information)"""
    return [{"username": user.username, "email": user.email} for user in users_db]

@router.get("/me", dependencies=[Depends(JWTBearer())])
async def get_current_user(token = Depends(JWTBearer())):
    """Get current user information"""
    # This is a simplified version - in a real app, you'd decode the token
    # and return the current user's information
    return {"message": "Current user info"}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    # Check if username already exists
    existing_user = get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create the user
    user = create_user(user_data)
    
    return {"message": "User created successfully"}
