from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class MusicBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    artist: str = Field(..., min_length=1, max_length=120)
    genre: str = Field(..., min_length=1, max_length=80)
    release_year: int = Field(..., ge=1900, le=2100)

    @field_validator("title", "artist", "genre")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Campo nao pode ser vazio.")
        return cleaned


class MusicCreate(MusicBase):
    pass


class MusicUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    artist: str | None = Field(default=None, min_length=1, max_length=120)
    genre: str | None = Field(default=None, min_length=1, max_length=80)
    release_year: int | None = Field(default=None, ge=1900, le=2100)

    @field_validator("title", "artist", "genre")
    @classmethod
    def strip_optional_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return value

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Campo nao pode ser vazio.")
        return cleaned

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "MusicUpdate":
        if all(
            value is None
            for value in (
                self.title,
                self.artist,
                self.genre,
                self.release_year,
            )
        ):
            raise ValueError("O ultimo campo deve ser preenchido.")

        return self


class MusicResponse(MusicBase):
    id: str
