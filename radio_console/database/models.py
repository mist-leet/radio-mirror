from __future__ import annotations
from enum import Enum as PythonEnum
from typing import List, Dict, Any, Type
from sqlalchemy import ForeignKey, select, and_, func
from sqlalchemy import Text, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from sqlalchemy.sql.elements import KeyedColumnElement
from connection import Session
from radio_console.utils.base import classproperty


class Base(DeclarativeBase):

    @classmethod
    def get_or_create(cls, relations: List[Base], data: Dict[str, Any]) -> Base:
        data = {
            key: value
            for key, value in data.items()
            if key in cls.field_names + cls.relation_names
        }
        relation_map = {}
        for obj in relations:
            if not cls.relations.get(obj.table_name):
                continue
            relation_map[obj.table_name] = obj
            data[obj.table_name] = obj
        where_conditions = []
        for field in cls.fields:
            if field.name == 'id' or bool(field.foreign_keys) or field.name not in data:
                continue
            where_conditions.append((field == data.get(field.name)))
        for field_name, relation_object in relation_map.items():
            if relation_object.id is None:
                continue
            where_conditions.append((getattr(cls, field_name) == relation_object))
        query = select(cls).where(and_(*where_conditions)).limit(1)
        with Session() as session:
            result = session.scalars(query).first()
            return result or cls.__create(data)

    @classmethod
    def get(cls, id: int) -> Base:
        with Session() as session:
            query = select(cls).where(cls.id == id).limit(1)
            result = session.scalars(query).first()
            return result

    @classmethod
    def __create(cls, data: dict) -> Base:
        with Session() as session:
            obj = cls(**data)
            session.add(obj)
            session.commit()
            return cls.get(obj.id)

    @classproperty
    def fields(cls) -> ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]:
        return cls.__table__.columns

    @classproperty
    def field_names(cls) -> List[str]:
        return list(cls.__table__.columns.keys())

    @classproperty
    def relation_names(cls) -> List[str]:
        return list(cls.__mapper__.relationships.keys())

    @classproperty
    def relations(cls):
        return cls.__mapper__.relationships

    @classproperty
    def table_name(cls) -> List[str]:
        return cls.__tablename__

    @classmethod
    def random(cls, amount: int) -> List[Base]:
        with Session() as session:
            query = select(cls).order_by(func.random()).limit(amount)
            return session.scalars(query).all()

    def __str__(self) -> str:
        return str(self.as_dict())

    def __repr__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name)
            for column in self.fields
        }


class Artist(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())

    albums: Mapped[List[Album]] = relationship(back_populates='artist')
    tracks: Mapped[List[Track]] = relationship(back_populates='artist')


class Album(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())
    year: Mapped[int] = mapped_column(Integer())
    path: Mapped[str] = mapped_column(Text())
    artist_id: Mapped[int] = mapped_column(ForeignKey('artist.id'))

    artist: Mapped[Artist] = relationship(back_populates='albums')
    tracks: Mapped[List[Track]] = relationship(back_populates='album')


class Track(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())
    track_number: Mapped[int] = mapped_column(Integer())
    filename: Mapped[str] = mapped_column(Text())
    artist_id: Mapped[int] = mapped_column(ForeignKey('artist.id'), nullable=False)
    album_id: Mapped[int] = mapped_column(ForeignKey('album.id'), nullable=False)

    artist: Mapped[Artist] = relationship(back_populates='tracks')
    album: Mapped[Album] = relationship(back_populates='tracks')

    @property
    def full_path(self) -> str:
        return f'{self.album.path}/{self.filename}'


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())


class EntityTag(Base):
    __tablename__ = 'entity_tag'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entity_id: Mapped[int] = mapped_column(Integer())
    entity_type: Mapped[int] = mapped_column(Integer())
    tag_id: Mapped[int] = mapped_column(Integer())


class EntityType(PythonEnum):
    track = 1
    album = 2
    aritst = 3

    def model(self) -> Type[Base]:
        return {
            EntityType.track: Track,
            EntityType.album: Album,
            EntityType.aritst: Artist,
        }.get(self)

    @classmethod
    def get_model(cls, type: int) -> Type[Base]:
        return cls(type).model()

