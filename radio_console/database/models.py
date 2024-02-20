from __future__ import annotations
from dataclasses import dataclass, fields as dataclass_fields, asdict, field
from base import classproperty


@dataclass(frozen=True)
class BaseModel:

    @classproperty
    def fields(cls, include_id: bool = True) -> list[str]:
        fields = [field.name for field in dataclass_fields(cls)]
        if include_id:
            return fields
        return [field for field in fields if field != 'id']

    @classmethod
    def _to_snake_case(cls, text: str) -> str:
        result = [text[0].lower()]
        for char in text[1:]:
            if char.isupper():
                result.append('_')
                result.append(char.lower())
            else:
                result.append(char)
        return ''.join(result)

    @classproperty
    def table(cls) -> str:
        return cls._to_snake_case(cls.__name__)

    @classmethod
    def from_dict(cls, data: dict) -> BaseModel:
        return cls(**data)

    def to_dict(self, filter_none: bool = False) -> dict:
        if not filter_none:
            return asdict(self)
        return {
            k: v
            for k, v in asdict(self).items()
            if v is not None
        }


@dataclass(frozen=True)
class Artist(BaseModel):
    id: int | None = field(default=None)
    name: str | None = field(default=None)


@dataclass(frozen=True)
class Album(BaseModel):
    id: int | None = field(default=None)
    name: str | None = field(default=None)
    year: int | None = field(default=None)
    path: str | None = field(default=None)
    artist_id: int | None = field(default=None)


@dataclass(frozen=True)
class Genre(BaseModel):
    id: int | None = field(default=None)
    name: str | None = field(default=None)


@dataclass(frozen=True)
class Vibe(BaseModel):
    id: int | None = field(default=None)
    name: str | None = field(default=None)


@dataclass(frozen=True)
class Track(BaseModel):
    id: int | None = field(default=None)
    name: str | None = field(default=None)
    track_number: int | None = field(default=None)
    artist_id: int | None = field(default=None)
    album_id: int | None = field(default=None)
    genre_id: int | None = field(default=None)
    year: int | None = field(default=None)
    comment: str | None = field(default=None)
    rating: int | None = field(default=None)
    filename: str | None = field(default=None)


@dataclass(frozen=True)
class TrackVibe(BaseModel):
    id: int | None = field(default=None)
    track_id: int | None = field(default=None)
    vibe_id: int | None = field(default=None)


TModel = Artist | Album | Genre | Vibe | Track | TrackVibe
