from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from typing import Iterator

from radio_console.utils import env_config
from radio_console.database import CRUD, Artist, Album, Track, TrackVibe, Vibe

__all__ = ('MetadataParser', )

class MetadataParser:

    source_path: str = env_config.get('SOURCE_PATH')
    meta_file_name = 'meta.json'

    @classmethod
    def run(cls):
        result_log = {}
        for meta_path in cls.__meta_files():
            with open(meta_path, 'r', encoding='utf-8') as file:
                meta_data = json.load(file)
                processor = SongDataProcessor(
                    vibe_info=meta_data['vibe'],
                    artist_info=meta_data['artist'],
                    album_info=meta_data['album'],
                    track_list_info=meta_data['track_list'],
                )
                processor.run()
                result_log[meta_path] = processor.log
        return result_log

    @classmethod
    def __meta_files(cls) -> Iterator[str]:
        for root, dirs, files in os.walk(cls.source_path):
            for file in files:
                if file == cls.meta_file_name:
                    yield os.path.join(root, file)


@dataclass
class SongDataProcessor:
    vibe_info: str
    artist_info: dict
    album_info: dict
    track_list_info: list[dict]

    vibe: Vibe = field(default=None, init=False)
    artist: Artist = field(default=None, init=False)
    album: Album = field(default=None, init=False)
    track_list: list[Track] = field(default=None, init=False)
    __log: dict[str, int] = field(default_factory=dict, init=False)

    def __post_init__(self):
        self.vibe = CRUD.find(Vibe(name=self.vibe_info))
        if not self.vibe:
            raise KeyError(f'{self.vibe_info=} not found')

    @property
    def log(self) -> dict:
        return self.__log

    def run(self):
        self._process_artist()
        self._process_album()
        self._process_track_list()

    def _process_artist(self):
        self.artist = CRUD.find(Artist(
            name=self.artist_info['name']
        ))
        if not self.artist:
            self.__log['artist'] = 1
            self.artist = CRUD.create(Artist(name=self.artist_info['name']))

    def _process_album(self):
        self.album = CRUD.find(Album(
            name=self.album_info['name'],
            artist_id=self.artist.id
        ))
        if not self.album:
            self.__log['album'] = 1
            self.album = CRUD.create(Album(
                name=self.album_info['name'],
                year=self.album_info['year'],
                path=self.album_info['path'],
                artist_id=self.artist.id,
            ))

    def _process_track_list(self):
        for row in self.track_list_info:
            if CRUD.find(Track(
                artist_id=self.artist.id,
                album_id=self.album.id,
                name=row['name']
            )):
                continue
            track = CRUD.create(Track(
                name=row['name'],
                track_number=row['track_number'],
                artist_id=self.artist.id,
                album_id=self.album.id,
                year=self.album_info['year'],
                filename=row['filename'],
            ))
            CRUD.create(TrackVibe(
                track_id=track.id,
                vibe_id=self.vibe.id,
            ))
            self.__log['track'] = self.__log.get('track', 0) + 1

