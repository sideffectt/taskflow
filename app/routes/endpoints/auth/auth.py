from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends

from app.models import UserCreate, UserLogin, UserUpdate, UserResponse, Token
from app.services import get_user_by_username, get_user_by_email, create_user, authenticate_user, update_user
from app.config.security import create_access_token, get_current_user, get_current_user_with_role
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
        password=user.password,
        role=user.role.value
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


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user_with_role)):
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(user_data: UserUpdate, current_user: dict = Depends(get_current_user_with_role)):
    updated_user = update_user(current_user["username"], user_data.model_dump())
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user