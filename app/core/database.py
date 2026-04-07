from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoDatabase:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


mongo = MongoDatabase()


async def connect_to_mongo() -> None:
    mongo.client = AsyncIOMotorClient(settings.mongodb_url)
    mongo.database = mongo.client[settings.mongodb_db]
    await mongo.client.admin.command("ping")


async def close_mongo_connection() -> None:
    if mongo.client is not None:
        mongo.client.close()
        mongo.client = None
        mongo.database = None


def get_database() -> AsyncIOMotorDatabase:
    if mongo.database is None:
        raise RuntimeError("Conexão com o banco de dados não estabelecida.")

    return mongo.database
