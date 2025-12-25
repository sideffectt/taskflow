from fastapi import APIRouter, Depends
from typing import List

from app.models import TaskCreate, TaskUpdate, TaskResponse
from app.services import create_task, get_all_tasks, get_task_by_id, update_task, delete_task
from app.config import TaskNotFoundException
from app.config.security import get_current_user

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=201)
async def create_new_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    result = create_task(
        title=task.title,
        description=task.description,
        priority=task.priority
    )
    return result


@router.get("", response_model=List[TaskResponse])
async def list_tasks(current_user: str = Depends(get_current_user)):
    return get_all_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, current_user: str = Depends(get_current_user)):
    task = get_task_by_id(task_id)
    if not task:
        raise TaskNotFoundException(task_id)
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: str, task: TaskUpdate, current_user: str = Depends(get_current_user)):
    result = update_task(task_id, task.model_dump())
    if not result:
        raise TaskNotFoundException(task_id)
    return result


@router.delete("/{task_id}", status_code=204)
async def delete_existing_task(task_id: str, current_user: str = Depends(get_current_user)):
    success = delete_task(task_id)
    if not success:
        raise TaskNotFoundException(task_id)
    return None