from typing import List
from sqlalchemy import select
from radio_console.database.connection import Session
from radio_console.database.models import Track, Album
from radio_console.console.player import Mount, PlayerMount, Mode
from radio_console.console.metadata import MetaParser


class ConsoleEngine:

    @classmethod
    def update_queue(cls, mount: Mount, amount: int):
        player_mount = PlayerMount.get(mount)
        if player_mount.config.mode == Mode.album:
            with Session() as session:
                albums: List[Album] = session.scalars(Album.random(10)).all()
                album_ids = [row.id for row in albums]
                tracks = session.scalars(select(Track).where(Track.album_id == album_ids).limit(amount))
        elif player_mount.config.mode == Mode.default:
            tracks = Track.random(amount)
        else:
            raise KeyError(f'No registered config.mode: {player_mount.config.mode}')
        player_mount.update(tracks)

    @classmethod
    def update_db(cls):
        MetaParser.run()
