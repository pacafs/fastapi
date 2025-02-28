# =========================================
# Authentication Routes
# =========================================
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
## Modules
from app.auth.users import Token
from app.auth.jwt_handler import create_access_token
from app.auth.users import LoginRequest, UserResponse, authenticate_user, create_user, get_user_by_email
from db.user import UserCreate


router = APIRouter()


@router.post(
    "/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with username, email, and password"
)
def register_user(user: UserCreate):
    """
    User registration endpoint
    
    Creates a new user account with the provided information.
    Checks if the email is already registered to prevent duplicates.
    
    Args:
        user (UserCreate): User data including username, email, and password
        
    Returns:
        UserResponse: The created user without sensitive information
        
    Raises:
        HTTPException: If email is already registered
    """
    # Check if email already exists
    if get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = create_user(user)
    
    # Return user info (excluding password)
    return UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Login with username and password to get access token"
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User login endpoint
    
    Authenticates a user with username and password,
    and returns a JWT token on success.
    
    Args:
        form_data (OAuth2PasswordRequestForm): Username and password form data
        
    Returns:
        Token: JWT access token for authenticated requests
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    
    # Check if authentication failed
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with 30-minute expiration
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires=access_token_expires
    )
    
    # Return the token response
    return {"access_token": access_token["access_token"], "token_type": "bearer"}


@router.post(
    "/login-json",
    response_model=Token,
    summary="User login with JSON",
    description="Login with username and password (JSON format) to get access token"
)
def login_json(login_data: LoginRequest):
    """
    User login endpoint (JSON format)
    
    Authenticates a user with username and password from JSON body,
    and returns a JWT token on success.
    
    This is an alternative to the standard /login endpoint that uses form data.
    
    Args:
        login_data (LoginRequest): JSON with username and password
        
    Returns:
        Token: JWT access token for authenticated requests
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = authenticate_user(login_data.username, login_data.password)
    
    # Check if authentication failed
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with 30-minute expiration
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires=access_token_expires
    )
    
    # Return the token response
    return {"access_token": access_token["access_token"], "token_type": "bearer"}
