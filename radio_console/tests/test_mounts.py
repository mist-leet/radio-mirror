from unittest import TestCase

from sqlalchemy import text

from player import Mount, PlayerMount, Config, Mode
from radio_console.database.connection import Session
from radio_console.tests import init_db
from radio_console.database.models import Artist, Album, Track
init_db()

class TestMounts(TestCase):

    def init_song_data(self, n: int):
        with Session() as session:
            artist = Artist.get_or_create([], {'name': f'test_artist_{n}'})
            album = Album.get_or_create([artist],
                                        {'name': f'test_album_{n}', 'year': 2020, 'path': 'f/test_{n}/'})
            tracks = [Track.get_or_create(
                [artist, album],
                {'name': f'test_{i}', 'track_number': i, 'filename': f'test_{i}'}
            ) for i in range(300)]
            session.add_all(tracks)
            session.commit()

    def tearDown(self):
        with Session() as session:
            session.execute(text("""
                delete from track CASCADE;
                delete from album CASCADE;
                delete from artist CASCADE;
            """))
            session.commit()

    def setUp(self):
        self.init_song_data(1)
        self.init_song_data(2)
        self.init_song_data(3)

    def test_config_default(self):
        player = PlayerMount(Mount.default(), Config(mode=Mode.default))
        result = player.all()
        artist_ids = [row.artist.id for row in result]
        self.assertTrue(len(set(artist_ids)) > 1)

    def test_config_album(self):
        player = PlayerMount(Mount.default(), Config(mode=Mode.album))
        result = player.all()
        artist_ids = [row.artist.id for row in result]
        self.assertTrue(len(set(artist_ids)) == 1)

