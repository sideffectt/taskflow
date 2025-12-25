from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings, db
from app.routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield
    db.disconnect()
    
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

app.include_router(api_router)

@app.get('/')
def root():
    return{'message': f'{settings.app_name} is running'}


