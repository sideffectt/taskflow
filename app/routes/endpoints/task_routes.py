from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from typing import List

from app.models import TaskCreate, TaskUpdate, TaskResponse
from app.services import create_task, get_all_tasks, get_task_by_id, update_task, delete_task, generate_tasks_pdf
from app.config import TaskNotFoundException
from app.config.security import get_current_user

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=201)
async def create_new_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    return create_task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        user_id=current_user
    )


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: str = Depends(get_current_user)
):
    return get_all_tasks(user_id=current_user, skip=skip, limit=limit)


@router.get("/export/pdf")
async def export_tasks_pdf(current_user: str = Depends(get_current_user)):
    tasks = get_all_tasks(user_id=current_user, limit=500)
    pdf_buffer = generate_tasks_pdf(tasks, current_user)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=tasks_{current_user}.pdf"}
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, current_user: str = Depends(get_current_user)):
    task = get_task_by_id(task_id, current_user)
    if not task:
        raise TaskNotFoundException(task_id)
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: str, task: TaskUpdate, current_user: str = Depends(get_current_user)):
    result = update_task(task_id, current_user, task.model_dump())
    if not result:
        raise TaskNotFoundException(task_id)
    return result


@router.delete("/{task_id}", status_code=204)
async def delete_existing_task(task_id: str, current_user: str = Depends(get_current_user)):
    success = delete_task(task_id, current_user)
    if not success:
        raise TaskNotFoundException(task_id)
    return None
