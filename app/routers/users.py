from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from app.models.user import User, UserCreate, UserResponse, TokenResponse, LoginRequest, RefreshToken, RefreshRequest
from db.database import pgSession
from app.utils.auth.utils import hash_password, verify_password
from app.utils.auth.jwt.jwt_handler import create_access_token, create_tokens, decode_token, create_refresh_token
from app.utils.auth.jwt.jwt_bearer import JWTBearer, decode_token
from typing import List, Annotated, cast
from datetime import datetime

router = APIRouter()
# Create a JWT bearer instance
jwt_bearer = JWTBearer()
# Create a dependency to check the token
checkToken = Annotated[str, Depends(jwt_bearer)]


# @router.get('', response_model=List[UserResponse])
# def get_users(token: checkToken, session: pgSession):
#     """Get all users (without sensitive information)"""
#     return session.exec(select(User)).all()

@router.get('/me', response_model=UserResponse)
def get_me(token: checkToken, session: pgSession):
    """Get the current user"""
    # Decode the token to get user information
    user_info = decode_token(token)
    # Extract user_id from the decoded token
    user_id = user_info.get("user_id")  

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/register", status_code=201, response_model=UserResponse)
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


@router.post("/login", status_code=200, response_model=TokenResponse)
def login_user(login_data: LoginRequest, session: pgSession):
    """Login a user and return JWT tokens"""
    # Find the user in the database
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    
    # If user not found or password doesn't match
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Ensure user.id is not None
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User ID is not set"
        )
    
    # Generate tokens
    tokens = create_tokens(data={"sub": user.username, "user_id": user.id})
    
    # Store refresh token in database
    refresh_token, expires_at = create_refresh_token()
    db_refresh_token = RefreshToken(
        token=tokens["refresh_token"],
        expires_at=expires_at,
        user_id=cast(int, user.id)  # Cast to satisfy type checker
    )
    
    session.add(db_refresh_token)
    session.commit()
    
    return tokens

@router.post("/logout", status_code=200)
def logout_user(token: checkToken, refresh_request: RefreshRequest, session: pgSession):
    """Logout a user by revoking their refresh token"""
    # Revoke the refresh token
    db_token = session.exec(
        select(RefreshToken).where(
            RefreshToken.token == refresh_request.refresh_token
        )
    ).first()
    
    # If token found, mark it as revoked
    if db_token:
        db_token.revoked = True
        session.add(db_token)
        session.commit()
    
    return {"message": "Successfully logged out"}



@router.post("/refresh", status_code=200, response_model=TokenResponse)
def refresh_token(refresh_request: RefreshRequest, session: pgSession):
    """Refresh access token using a valid refresh token"""
    # Find the refresh token in the database
    db_token = session.exec(
        select(RefreshToken).where(
            RefreshToken.token == refresh_request.refresh_token,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        )
    ).first()
    
    # If token not found, expired, or revoked
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Get the user
    user = session.get(User, db_token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Ensure user.id is not None
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User ID is not set"
        )
    
    # Revoke the current refresh token
    db_token.revoked = True
    session.add(db_token)
    
    # Generate new tokens
    tokens = create_tokens(data={"sub": user.username, "user_id": user.id})
    
    # Store new refresh token in database
    refresh_token, expires_at = create_refresh_token()
    new_db_refresh_token = RefreshToken(
        token=tokens["refresh_token"],
        expires_at=expires_at,
        user_id=cast(int, user.id)  # Cast to satisfy type checker
    )
    
    session.add(new_db_refresh_token)
    session.commit()
    # The function returns a dictionary containing the new access token and refresh token for the user.
    # {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}
    return tokens
