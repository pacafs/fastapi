import time
import jwt
from typing import Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
import os
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =========================================
# JWT Configuration
# =========================================
# Get JWT configuration from environment variables
JWT_SECRET = os.getenv("JWT_SECRET", "fallback_secret_for_development_only")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "1800"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def token_response(access_token: str, refresh_token: Optional[str] = None, expires_in: Optional[int] = None) -> Dict[str, Any]:
    """
    Create a standard response format for JWT tokens
    
    Args:
        access_token (str): The encoded JWT access token
        refresh_token (str, optional): The refresh token
        expires_in (int, optional): Token expiration time in seconds
        
    Returns:
        dict: A dictionary containing the token and its type
    """
    response: Dict[str, Any] = {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    if refresh_token:
        response["refresh_token"] = refresh_token
    
    if expires_in:
        response["expires_in"] = expires_in
    
    return response


def create_access_token(data: dict, expires: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token
    
    Args:
        data (dict): Payload data to be encoded in the token
        expires (Optional[timedelta], optional): Custom expiration time. 
                                                  Defaults to None.
    
    Returns:
        str: The JWT token
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()
    
    # Set token expiration time
    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    
    # Add the expiration claim to the token payload
    to_encode.update({"exp": int(expire.timestamp())})
    
    # Encode the JWT token
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return encoded_jwt


def create_refresh_token() -> Tuple[str, datetime]:
    """
    Create a new refresh token
    
    Returns:
        Tuple[str, datetime]: The refresh token and its expiration date
    """
    # Generate a unique token
    token = str(uuid.uuid4())
    
    # Set expiration date
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    return token, expires_at


def create_tokens(data: dict) -> dict:
    """
    Create both access and refresh tokens
    
    Args:
        data (dict): Payload data to be encoded in the access token
        
    Returns:
        dict: Dictionary containing both tokens and metadata
    """
    # Create access token
    access_token = create_access_token(data)
    
    # Create refresh token
    refresh_token, _ = create_refresh_token()
    
    # Calculate expiration in seconds
    expires_in = ACCESS_TOKEN_EXPIRE_SECONDS
    
    return token_response(access_token, refresh_token, expires_in)


def decode_token(token: str) -> Dict:
    """
    Decode and validate a JWT token
    
    Args:
        token (str): The JWT token to decode
        
    Returns:
        Dict: The decoded token payload if valid, empty dict otherwise
    """
    try:
        # Decode the token
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Check if the token has expired
        if decoded_token["exp"] >= time.time():
            return decoded_token
        
        # Token has expired
        return {}
    except:
        # If there's any error during decoding, return an empty dict
        return {} 

