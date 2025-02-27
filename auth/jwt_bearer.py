from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .jwt_handler import decode_token

class JWTBearer(HTTPBearer):
    """
    JWT Bearer security scheme
    
    This class implements JWT token validation for protected routes.
    It inherits from FastAPI's HTTPBearer class to handle Bearer token authentication.
    """
    
    def __init__(self, auto_error: bool = True):
        """
        Initialize the JWT Bearer security scheme
        
        Args:
            auto_error (bool, optional): Whether to auto-raise exceptions on missing credentials. 
                                        Defaults to True.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        """
        Validate JWT token from the request
        
        This method is called automatically by FastAPI when the dependency is used.
        It extracts and validates the JWT token from the Authorization header.
        
        Args:
            request (Request): The FastAPI request object
            
        Returns:
            str: The decoded JWT token
            
        Raises:
            HTTPException: If the token is invalid, expired, or missing
        """
        credentials: Optional[HTTPAuthorizationCredentials] = await super(JWTBearer, self).__call__(request)
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code."
            )
            
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme. Use Bearer."
            )
            
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token or expired token."
            )
            
        return credentials.credentials

    def verify_jwt(self, token: str) -> bool:
        """
        Verify the JWT token validity
        
        Args:
            token (str): The JWT token to verify
            
        Returns:
            bool: True if the token is valid, False otherwise
        """
        try:
            # Decode and validate the token
            payload = decode_token(token)
            
            # If payload is empty, token is invalid or expired
            return bool(payload)
        except Exception:
            return False 