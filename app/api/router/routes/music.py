from fastapi import APIRouter, Depends, Response, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.repositories.music_repository import MusicRepository
from app.schemas.music import MusicCreate, MusicResponse, MusicUpdate
from app.services.music_service import MusicService


router = APIRouter(prefix="/musics", tags=["Musics"])


def get_music_service(
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> MusicService:
    return MusicService(MusicRepository(database))


@router.post(
    "/",
    response_model=MusicResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_music(
    payload: MusicCreate,
    service: MusicService = Depends(get_music_service),
) -> dict[str, str | int]:
    return await service.create_music(payload)


@router.get("/", response_model=list[MusicResponse])
async def list_musics(
    service: MusicService = Depends(get_music_service),
) -> list[dict[str, str | int]]:
    return await service.list_musics()


@router.get("/{music_id}", response_model=MusicResponse)
async def get_music(
    music_id: str,
    service: MusicService = Depends(get_music_service),
) -> dict[str, str | int]:
    return await service.get_music_by_id(music_id)


@router.patch("/{music_id}", response_model=MusicResponse)
async def update_music(
    music_id: str,
    payload: MusicUpdate,
    service: MusicService = Depends(get_music_service),
) -> dict[str, str | int]:
    return await service.update_music(music_id, payload)


@router.delete("/{music_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_music(
    music_id: str,
    service: MusicService = Depends(get_music_service),
) -> Response:
    await service.delete_music(music_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
