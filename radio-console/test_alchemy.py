import string
import random
from unittest import TestCase

from sqlalchemy import text

from database.connection import DatabaseEngine, engine

assert engine is not None

from database.models import Base

DatabaseEngine.create_tables_if_need(engine, Base)

from console.metadata import MetaParser

# MetaParser.run()
from database.models import *
from database.connection import Session


class TestAlchemy(TestCase):

    def __clear_all(self):
        with Session() as session:
            session.execute(text("""
                delete from track CASCADE;
                delete from album CASCADE;
                delete from artist CASCADE;
            """))
            session.commit()

    @classmethod
    def gen_str(cls, length: int = 4) -> str:
        return random.sample(string.ascii_lowercase, length)

    def setUp(self) -> None:
        self.__clear_all()

    def test_add_tags(self):
        artist = Artist.get_or_create([], {'name': 'test_artist_2'})
        album = Album.get_or_create([artist], {'name': 'test_album_2', 'year': 2020, 'path': '/test/'})
        tracks = [
            Track.get_or_create([artist, album], {'name': f'test_{i}', 'track_number': i, 'filename': f'test_{i}'})
            for i in range(5)
        ]


    def test_add_another_one(self):
        with Session() as session:
            artist = Artist.get_or_create([], {'name': 'test_artist'})
            album = Album.get_or_create([artist], {'name': 'test_album', 'year': 2020, 'path': '/test/'})
            track = Track.get_or_create([artist, album], {'name': 'test', 'track_number': 1, 'filename': 'test'})
            track = Track.get_or_create([artist, album], {'name': 'test_2', 'track_number': 1, 'filename': 'test'})
            session.add_all([track])
            session.commit()
