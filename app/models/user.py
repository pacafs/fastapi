from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True): # type: ignore
    __tablename__ = "users" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str = Field(index=True)

class RefreshToken(SQLModel, table=True): # type: ignore
    __tablename__ = "refresh_tokens" # type: ignore
    
    id: int | None = Field(default=None, primary_key=True)
    token: str = Field(index=True, unique=True)
    expires_at: datetime = Field(index=True)
    revoked: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class RefreshRequest(BaseModel):
    refresh_token: str