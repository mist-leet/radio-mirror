import os
from unittest import TestCase

from crud import CRUD
from models import *
from radio_console.database.connection import DatabaseEngine


class TestDataBaseEngine(DatabaseEngine):
    _init_path = os.path.join(os.path.dirname(__file__), '../database/sql/init.sql')


cursor = TestDataBaseEngine.create()
TestDataBaseEngine.after_create(cursor)


class TestAlchemy(TestCase):

    def __clear_all(self):
        cursor.execute("""
            delete from track CASCADE;
            delete from album CASCADE;
            delete from artist CASCADE;
        """)

    def setUp(self) -> None:
        TestDataBaseEngine._init_database(cursor)

    def test_add_another_one(self):
        artist = CRUD.create(Artist(name='test_artist'))
        album = CRUD.create(Album(name='test_album', year=2020, path='/test/', artist_id=artist.id))
        tracks = [
            CRUD.create(Track(name='test', track_number=1, filename='test', artist_id=artist.id, album_id=album.id)),
            CRUD.create(Track(name='test2', track_number=1, filename='test', artist_id=artist.id, album_id=album.id))
        ]
        assert artist.to_dict() == CRUD.read(Artist(id=artist.id)).to_dict()
        assert album.to_dict() == CRUD.read(Album(id=album.id)).to_dict()
        assert tracks[0].to_dict() == CRUD.read(Track(id=tracks[0].id)).to_dict()
        assert tracks[1].to_dict() == CRUD.read(Track(id=tracks[1].id)).to_dict()
