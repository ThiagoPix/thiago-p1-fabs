from bson import ObjectId
from fastapi import HTTPException, status

from app.models.music import music_serializer
from app.repositories.music_repository import MusicRepository
from app.schemas.music import MusicCreate, MusicUpdate


class MusicService:
    def __init__(self, repository: MusicRepository) -> None:
        self.repository = repository

    async def create_music(self, payload: MusicCreate) -> dict[str, str | int]:
        music = await self.repository.create(payload.model_dump())
        return music_serializer(music)

    async def list_musics(self) -> list[dict[str, str | int]]:
        musics = await self.repository.list_all()
        return [music_serializer(music) for music in musics]

    async def get_music_by_id(self, music_id: str) -> dict[str, str | int]:
        object_id = self._parse_object_id(music_id)
        music = await self.repository.find_by_id(object_id)

        if music is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Musica não encontrada.",
            )

        return music_serializer(music)

    async def update_music(
        self,
        music_id: str,
        payload: MusicUpdate,
    ) -> dict[str, str | int]:
        object_id = self._parse_object_id(music_id)
        existing_music = await self.repository.find_by_id(object_id)

        if existing_music is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Musica não encontrada.",
            )

        updated_music = await self.repository.update(
            object_id,
            payload.model_dump(exclude_unset=True, exclude_none=True),
        )

        if updated_music is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao atualizar a musica.",
            )

        return music_serializer(updated_music)

    async def delete_music(self, music_id: str) -> None:
        object_id = self._parse_object_id(music_id)
        was_deleted = await self.repository.delete(object_id)

        if not was_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Musica não encontrada.",
            )

    @staticmethod
    def _parse_object_id(music_id: str) -> ObjectId:
        if not ObjectId.is_valid(music_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id da musica é inválido.",
            )

        return ObjectId(music_id)
