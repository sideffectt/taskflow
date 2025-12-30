from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.models import UserResponse, UserRoleUpdate
from app.services import get_all_users, get_user_by_username, update_user_role
from app.config.security import require_admin

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
async def list_all_users(current_user: dict = Depends(require_admin)):
    return get_all_users()


@router.put("/users/{username}/role", response_model=UserResponse)
async def change_user_role(username: str, role_data: UserRoleUpdate, current_user: dict = Depends(require_admin)):
    if username == current_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_user = update_user_role(username, role_data.role.value)
    return updated_user