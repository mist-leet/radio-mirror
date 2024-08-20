import os
import unittest

from radio_console.console import Config, QueueMode, Console
from radio_console.database import DatabaseEngine
from radio_console.database import Artist, Album, Track, TrackVibe, Vibe, CRUD
from radio_console.utils import Mount


class TestDataBaseEngine(DatabaseEngine):
    _init_path = os.path.join(os.path.dirname(__file__), '../database/sql/init.sql')


cursor = TestDataBaseEngine.create()
TestDataBaseEngine.after_create(cursor)


def init_test_data():
    test_data = {}
    for model in (TrackVibe, Track,  Album, Artist, Vibe):
        for row in CRUD.list(model(), 1_000):
            CRUD.delete(row)
    vibe_1 = CRUD.create(Vibe(name=Mount.tech.name))
    vibe_2 = CRUD.create(Vibe(name=Mount.ambient.name))
    test_data['vibe_1'] = vibe_1
    test_data['vibe_2'] = vibe_2
    artist_1 = CRUD.create(Artist(name='artist1'))
    artist_2 = CRUD.create(Artist(name='artist2'))
    test_data['artist_1'] = artist_1
    test_data['artist_2'] = artist_2
    album_1_1 = CRUD.create(Album(
        name='album1_1',
        year=2077,
        path='/www/test',
        artist_id=artist_1.id
    ))
    album_1_2 = CRUD.create(Album(
        name='album1_2',
        year=2077,
        path='/www/test',
        artist_id=artist_1.id
    ))
    album_2_1 = CRUD.create(Album(
        name='album2_1',
        year=2077,
        path='/www/test',
        artist_id=artist_1.id
    ))
    album_2_2 = CRUD.create(Album(
        name='album2_2',
        year=2077,
        path='/www/test',
        artist_id=artist_1.id
    ))
    test_data['album_1_1'] = album_1_1
    test_data['album_1_2'] = album_1_2
    test_data['album_2_1'] = album_2_1
    test_data['album_2_2'] = album_2_2
    test_data['tracks'] = []
    for album in [album_1_1, album_1_2, album_2_1, album_2_2]:
        for i in range(10):
            track = CRUD.create(Track(
                name=f'track_{album.name}_{i}',
                track_number=i,
                artist_id=album.artist_id,
                album_id=album.id,
                year=2077,
                comment='',
                rating=1,
                filename=f'{i}.mp3',
            ))
            test_data['tracks'].append(track)
            CRUD.create(TrackVibe(
                track_id=track.id,
                vibe_id=(
                    vibe_1.id if album in (album_1_1, album_2_1)
                    else vibe_2.id
                )
            ))


class TestConsole(unittest.TestCase):

    __test_data = {}

    def setUp(self):
        self.__test_data = init_test_data()

    def test_config_random(self):
        for mount in (Mount.tech, Mount.ambient):
            config = Config(QueueMode.random, mount, queue_amount=1_000)
            queue = Console.get_queue(config)




