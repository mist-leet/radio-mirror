from __future__ import annotations
from typing import List, Dict, Any
from typing import Optional
from sqlalchemy import ForeignKey, select, and_
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from database.connection import session


class Base(DeclarativeBase):

    @classmethod
    def get_or_create(cls, **kwargs) -> Base:
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class Artist(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())

    albums: Mapped[List['Album']] = relationship(back_populates='artist')
    tracks: Mapped[List['Track']] = relationship(back_populates='artist')

    @classmethod
    def get_or_create(cls, name: str) -> Artist:
        artist_query = select(Artist).where(Artist.name == name).limit(1)
        artist: Artist = session.scalars(artist_query).first()
        if not artist:
            return Artist(name=name)
        return artist


class Album(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())
    year: Mapped[int] = mapped_column(Integer())
    path: Mapped[str] = mapped_column(Text())
    artist_id: Mapped[int] = mapped_column(ForeignKey('artist.id'))

    artist: Mapped['Artist'] = relationship(back_populates='albums')
    tracks: Mapped['Track'] = relationship(back_populates='album')

    @classmethod
    def get_or_create(cls, name: str, artist: Artist, path: str, year: int) -> Album:
        if not artist.id:
            return Album(name=name, artist=artist, path=path, year=year)
        album_query = select(Album).where(and_(
            Album.name == name,
            Album.artist == artist,
            Album.year == year
        )).limit(1)
        album: Album = session.scalars(album_query).first()
        if not album:
            return Album(name=name, artist=artist, path=path, year=year)
        return album


class Track(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())
    track_number: Mapped[int] = mapped_column(Integer())
    filename: Mapped[str] = mapped_column(Text())
    artist_id: Mapped[int] = mapped_column(ForeignKey('artist.id'), nullable=False)
    album_id: Mapped[int] = mapped_column(ForeignKey('album.id'), nullable=False)

    artist: Mapped['Artist'] = relationship(back_populates='tracks')
    album: Mapped['Album'] = relationship(back_populates='tracks')

    @property
    def full_path(self) -> str:
        return f'{self.album.path}/{self.filename}'

    @classmethod
    def get_or_create(cls, name: str, track_number: int, filename: str, artist: Artist, album: Album) -> Track:
        if not artist.id or not album.id:
            return Track(
                name=name,
                track_number=track_number,
                filename=filename,
                artist=artist,
                album=album,
            )
        track_query = select(Track).where(and_(
            Track.name == name,
            Track.track_number == track_number,
            Track.filename == filename,
            Track.artist == artist,
            Track.album == album,
        )).limit(1)
        track: Track = session.scalars(track_query).first()
        if not track:
            return Track(
                name=name,
                track_number=track_number,
                filename=filename,
                artist_id=artist.id,
                album_id=album.id,
            )
        return track
