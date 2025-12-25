from datetime import timedelta
from fastapi import APIRouter, HTTPException, status

from app.models import UserCreate, UserLogin, UserResponse, Token
from app.services import get_user_by_username, get_user_by_email, create_user, authenticate_user
from app.config.security import create_access_token
from app.config.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate):
    if get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    if get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    new_user = create_user(
        username=user.username,
        email=user.email,
        password=user.password
    )
    return new_user


@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": authenticated_user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}