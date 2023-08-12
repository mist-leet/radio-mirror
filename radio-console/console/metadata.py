from __future__ import annotations
import json
import os
from dataclasses import asdict
from dataclasses import dataclass
from typing import Iterator, Union, Optional
from typing import List
from connection import Session
from database.models import Artist, Album, Track, Base
from utils.log import Logger


class MetaParser:
    # Путь до библиотеки с музыкой
    # source_path: str = r'/source'
    source_path: str = r'D:\prg_project\py\radio-tools\source'
    meta_file_name = 'meta.json'

    @classmethod
    def parse_meta(cls, meta: MetaData):
        artist = Artist.get_or_create([], asdict(meta.artist))
        album = Album.get_or_create([artist], asdict(meta.album))
        tracks = []
        for row in meta.track_list:
            tracks.append(Track.get_or_create([artist, album], asdict(row)))
        new_objects = cls.filter_new([artist, album, *tracks])
        if not new_objects:
            return
        with Session() as session:
            session.add_all(new_objects)
            session.commit()
        return [str(obj) for obj in new_objects]

    @classmethod
    def filter_new(cls, objects: List[Base]) -> List[Base]:
        return list(filter(lambda x: x.id is None, objects))

    @classmethod
    def run(cls) -> List[str]:
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
    def __extract_meta(cls, path: str) -> Optional[dict]:
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
class MetaData:
    artist: ArtistData
    album: AlbumData
    track_list: List[TrackData]

    @classmethod
    def from_dict(cls, data: dict) -> MetaData:
        return cls(
            artist=ArtistData(**data.get('artist', {})),
            album=AlbumData(**data.get('album', {})),
            track_list=[TrackData(**row) for row in data.get('track_list', [])],
        )


@dataclass
class ArtistData:
    name: str
    description: str
    tags: List[str]


@dataclass
class AlbumData:
    name: str
    description: str
    year: int
    tags: List[str]
    path: str


@dataclass
class TrackData:
    filename: str
    name: str
    duration: str
    tags: List[str]
    track_number: int
