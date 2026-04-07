from typing import Any


MUSIC_COLLECTION = "musics"


def music_serializer(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(document["_id"]),
        "title": document["title"],
        "artist": document["artist"],
        "genre": document["genre"],
        "release_year": document["release_year"],
    }
