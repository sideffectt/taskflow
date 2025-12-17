from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: int = Field(default=1, ge=1, le=5)
    
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    
class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: int
    created_at: datetime
    updated_at: datetime
    