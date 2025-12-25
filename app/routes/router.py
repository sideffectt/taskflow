from fastapi import APIRouter

from app.routes.endpoints.task_routes import router as task_router
from app.routes.endpoints.auth import auth_router

router = APIRouter()

router.include_router(task_router, prefix="/tasks", tags=["tasks"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])