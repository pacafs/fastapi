from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True): # type: ignore
    __tablename__ = "users" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    username: EmailStr = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str = Field(index=True)

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
    token_type: str