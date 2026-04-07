from fastapi import APIRouter

from app.api.router.routes.music import router as music_router


api_router = APIRouter()
api_router.include_router(music_router)
