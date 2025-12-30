from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.user


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserRoleUpdate(BaseModel):
    role: UserRole


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: Optional[UserRole] = UserRole.user
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str