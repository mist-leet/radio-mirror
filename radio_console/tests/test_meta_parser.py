import json
import os
import unittest

from radio_console.console import Config, QueueMode, Console
from radio_console.database import DatabaseEngine
from radio_console.database import Artist, Album, Track, TrackVibe, Vibe, CRUD
from radio_console.utils import Mount
from radio_console.meta._parser import SongDataProcessor


class TestDataBaseEngine(DatabaseEngine):
    _init_path = os.path.join(os.path.dirname(__file__), '../database/sql/init.sql')


cursor = TestDataBaseEngine.create()
TestDataBaseEngine.after_create(cursor)


class TestConsole(unittest.TestCase):
    __meta_data = [
        os.path.join(os.path.dirname(__file__), 'resources/meta_1.json'),
        os.path.join(os.path.dirname(__file__), 'resources/meta_2.json')
    ]

    def test_meta_parser(self):

        for meta_file_path in self.__meta_data:
            with open(meta_file_path, 'r', encoding='utf-8') as meta_file:
                meta_data = json.load(meta_file)
                SongDataProcessor(
                    vibe_info=meta_data['vibe'],
                    artist_info=meta_data['artist'],
                    album_info=meta_data['album'],
                    track_list_info=meta_data['track_list'],
                ).run()
                self.__assert(meta_data)

    def __assert(self, meta_data: dict):
        artist_info = meta_data['artist']
        artists = CRUD.list(Artist(name=artist_info['name']))
        assert len(artists) == 1
        assert artist_info['name'] == artists[0].name

        album_info = meta_data['album']
        albums = CRUD.list(Album(name=album_info['name']))
        assert len(albums) == 1
        assert album_info['name'] == albums[0].name

        track_list = meta_data['track_list']
        tracks = CRUD.list(Track())
        assert len(tracks) == len(track_list)
        for track_meta, track_db in zip(track_list, tracks):
            assert track_meta['name'] == track_db.name
