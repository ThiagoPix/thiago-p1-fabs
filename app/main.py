from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.api_router import api_router
from app.core.config import settings
from app.core.database import close_mongo_connection, connect_to_mongo, get_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["Root"])
async def read_root() -> dict[str, str]:
    return {
        "message": "Music CRUD API is running.",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    database = get_database()
    await database.command("ping")
    return {"status": "ok"}
