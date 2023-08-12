from typing import List
from sqlalchemy import select, func
from database.connection import Session
from database.models import Track
from console.player import Mount
from console.metadata import MetaParser


class ConsoleEngine:

    @classmethod
    def random_track(cls) -> Track:
        query = select(Track).order_by(func.random()).limit(1)
        track: Track = session.scalar(query)
        return track

    @classmethod
    def next(cls, mount: Mount) -> Track:
        ...

    @classmethod
    def queue(cls, mount: Mount, limit: int = 500) -> List[Track]:
        query = select(Track).order_by(func.random()).limit(limit)
        with Session() as session:
            return session.scalars(query).all()

    @classmethod
    def update_db(cls):
        MetaParser.run()
