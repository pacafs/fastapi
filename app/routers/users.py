from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.jwt.jwt_bearer import JWTBearer
from app.users.models import get_user_by_username
from app.models.user import UserCreate

router = APIRouter()

@router.get("/", dependencies=None)
async def get_users():
    """Get all users (without sensitive information)"""
    return ['All users']
