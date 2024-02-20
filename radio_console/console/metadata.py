from __future__ import annotations
import json
import os
from dataclasses import asdict, dataclass
from typing import Iterator

from radio_console.database.crud import CRUD
from radio_console.database.models import Artist, Album, Track

from radio_console.utils.log import Logger


class MetaParser:
    # Путь до библиотеки с музыкой
    # source_path: str = r'/source'
    source_path: str = r'//home/ilya/git/radio/source'
    meta_file_name = 'meta.json'

    @classmethod
    def parse_meta(cls, meta: MetaData):
        artist = CRUD.find(Artist(name=meta.artist.name))
        if not artist:
            artist = CRUD.create(Artist(name=meta.artist.name))
        album = CRUD.find(Album(
            name=meta.album.name,
            year=meta.album.year,
            artist_id=artist.id
        ))
        if not album:
            album = CRUD.create(Album(
                name=meta.album.name,
                year=meta.album.year,
                artist_id=artist.id,
                path=meta.album.path
            ))
        tracks = []
        for row in meta.track_list:
            track = CRUD.find(Track(
                name=row.name,
                track_number=row.track_number,
                artist_id=artist.id,
                album_id=album.id,
                filename=row.filename
            ))
            if not track:
                track = CRUD.create(Track(
                    name=row.name,
                    track_number=row.track_number,
                    artist_id=artist.id,
                    album_id=album.id,
                    filename=row.filename,
                ))
                tracks.append(track)
        return [str(obj) for obj in tracks]

    @classmethod
    def run(cls) -> list[str]:
        Logger.info(f'Start parsing meta info')
        result = []
        for meta in cls.__meta_iter():
            inserted = cls.parse_meta(meta)
            Logger.info(f'Inseted: {inserted}')
        return result

    @classmethod
    def __meta_iter(cls) -> Iterator[MetaData]:
        for path in cls.__source_directory_iter():
            meta_path = os.path.join(path, 'meta.json')
            meta_data = cls.__extract_meta(meta_path)
            if not meta_data:
                print(f'Не удалось загрузить: {meta_path}')
                continue
            meta_data['album_path'] = meta_path.replace('/meta.json', '')
            yield MetaData.from_dict(meta_data)

    @classmethod
    def __extract_meta(cls, path: str) -> dict | None:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    @classmethod
    def __source_directory_iter(cls) -> Iterator[str]:
        for root, dirs, files in os.walk(cls.source_path):
            print(root, dirs, files)
            yield from map(lambda dir_name: os.path.join(root, dir_name), dirs)



@dataclass
class ArtistData:
    name: str
    description: str
    tags: list[str]


@dataclass
class AlbumData:
    name: str
    description: str
    year: int
    tags: list[str]
    path: str


@dataclass
class TrackData:
    filename: str
    name: str
    duration: str
    tags: list[str]
    track_number: int

@dataclass
class MetaData:
    artist: ArtistData
    album: AlbumData
    track_list: list[TrackData]

    @classmethod
    def from_dict(cls, data: dict) -> MetaData:
        return cls(
            artist=ArtistData(**data.get('artist', {})),
            album=AlbumData(**data.get('album', {})),
            track_list=[TrackData(**row) for row in data.get('track_list', [])],
        )
