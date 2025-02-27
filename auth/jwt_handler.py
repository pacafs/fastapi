import time
import jwt  # You'll need to install PyJWT: pip install PyJWT
from typing import Dict, Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =========================================
# JWT Configuration
# =========================================
# Get JWT configuration from environment variables
JWT_SECRET = os.getenv("JWT_SECRET", "fallback_secret_for_development_only")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def token_response(token: str) -> dict:
    """
    Create a standard response format for JWT tokens
    
    Args:
        token (str): The encoded JWT token
        
    Returns:
        dict: A dictionary containing the token and its type
    """
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> dict:
    """
    Create a new JWT access token
    
    Args:
        data (dict): Payload data to be encoded in the token
        expires_delta (Optional[timedelta], optional): Custom expiration time. 
                                                       Defaults to None.
    
    Returns:
        dict: The token response containing the JWT token
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()
    
    # Set token expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add the expiration claim to the token payload
    to_encode.update({"exp": expire})
    
    # Encode the JWT token
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token_response(encoded_jwt)


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