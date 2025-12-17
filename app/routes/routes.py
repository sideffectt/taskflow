from fastapi import APIRouter, HTTPException
from typing import List

from app.models.models import TaskCreate, TaskUpdate, TaskResponse
from app.crud.crud import create_task, get_all_tasks, get_task_by_id, update_task, delete_task

router = APIRouter(prefix='/tasks', tags=['tasks']) #Create router 

@router.post("", response_model=TaskResponse, status_code=201)
def create_new_task(task: TaskCreate):
    result = create_task(
        title=task.title,
        description=task.description,
        priority=task.priority
    )
    return result

@router.get("", response_model=List[TaskResponse])
def list_tasks():
    return get_all_tasks()


@router.get('/{task_id}', response_model=TaskResponse)
def get_task(task_id: str):
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task

@router.put('/{task_id}', response_model=TaskResponse)
def update_existing_task(task_id: str, task: TaskUpdate):
    result = update_task(task_id, task.model_dump())
    if not result:
        raise HTTPException(status_code=404, detail='Task not found')
    return result

@router.delete('/{task_id}', status_code=204)
def delete_existing_task(task_id: str):
    success = delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail='Task not Found')
    return None

