from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import eyed3


@dataclass
class Meta:
    genre: str


@dataclass(frozen=True)
class TaggedData:
    _file: str = field(init=False)


@dataclass(frozen=True)
class Track:
    artist: str
    title: str
    comment: str
    duration: int
    genre: str
    album: 'Album'
    meta: Optional[Meta] = field(default=None)

    def to_dict(self) -> dict:
        return {
            'artist': self.artist,
            'title': self.title,
            'comment': self.comment,
            'duration': self.duration,
            'genre': self.genre,
        }


@dataclass(frozen=True)
class Album:
    title: str
    artist: str
    year: datetime
    image: str
    meta: Optional[Meta] = field(default=None)
    tracks: List[Track] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'artist': self.artist,
            'year': self.year,
            'image': self.image,
            'tracks': [track.to_dict() for track in self.tracks]
        }

    @classmethod
    def from_files(cls, files: List[str]) -> 'Album':
        meta = [eyed3.load(file) for file in files]
        track = meta[0]
        album = Album(
            title=track.tag.album,
            artist=track.tag.artist,
            year=track.tag.getBestDate(),
            image=''
        )
        for track in meta:
            album.tracks.append(Track(
                artist=track.tag.artist,
                title=track.tag.title,
                comment='',
                duration='',
                genre=track.tag.genre,
                album=album,
            ))
        return album


