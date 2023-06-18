from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Artist(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text())

    albums: Mapped[List['Album']] = relationship(back_populates='artist')
    tracks: Mapped[List['Track']] = relationship(back_populates='artist')


class Album(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    path: Mapped[str] = mapped_column(Text())
    artist_id: Mapped[int] = mapped_column(ForeignKey('artist.id'))

    artist: Mapped['Artist'] = relationship(back_populates='albums')
    tracks: Mapped['Track'] = relationship(back_populates='album')


class Track(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    track_number: Mapped[int] = mapped_column(Integer())
    year: Mapped[int] = mapped_column(Integer())
    filename: Mapped[str] = mapped_column(Text())
    artist_id: Mapped[int] = mapped_column(ForeignKey('artist.id'))
    album_id: Mapped[int] = mapped_column(ForeignKey('album.id'))

    artist: Mapped['Artist'] = relationship(back_populates='tracks')
    album: Mapped['Album'] = relationship(back_populates='tracks')
