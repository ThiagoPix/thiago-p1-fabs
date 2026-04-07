from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.music import MUSIC_COLLECTION


class MusicRepository:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.collection = database[MUSIC_COLLECTION]

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        result = await self.collection.insert_one(data)
        created_music = await self.find_by_id(result.inserted_id)
        if created_music is None:
            raise RuntimeError("Falha ao criar a musica.")
        return created_music

    async def list_all(self) -> list[dict[str, Any]]:
        cursor = self.collection.find().sort("title", 1)
        return await cursor.to_list(length=None)

    async def find_by_id(self, music_id: ObjectId) -> dict[str, Any] | None:
        return await self.collection.find_one({"_id": music_id})

    async def update(
        self,
        music_id: ObjectId,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        await self.collection.update_one({"_id": music_id}, {"$set": data})
        return await self.find_by_id(music_id)

    async def delete(self, music_id: ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": music_id})
        return result.deleted_count == 1
