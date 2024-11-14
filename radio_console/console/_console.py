from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache

from database import Track, build_track_info
from database import get_queue_random, playlist_paths, cover_path
from utils import find_cover
from ._config import Config, QueueMode


@dataclass(frozen=True)
class Console:
    config: Config

    @classmethod
    def get_queue(cls, config: Config) -> Queue:
        return cls(config=config).__process_queue()

    @classmethod
    @lru_cache(maxsize=10)
    def track_data(cls, track: Track) -> dict:
        result = build_track_info(track.id, track.album_id)
        return {
            'album': {
                'name': result[0]['album_name'],
                'year': result[0]['album_year'],
            },
            'artist': {
                'name': result[0]['artist_name'],
            },
            'track_list': [{
                'id': track['id'],
                'name': track['name'],
                'track_number': track['track_number'],
                'duration': track['duration'],
                'is_active': track['is_active'],
            } for track in result]
        }

    @classmethod
    @lru_cache(maxsize=10)
    def cover(cls, track: Track) -> str | None:
        path = cover_path(track)
        path = find_cover(path)
        if not cover_path:
            raise KeyError(f'No cover for {track=}')
        return path

    def __process_queue(self) -> Queue:
        if self.config.queue_mode == QueueMode.random:
            return self.__process_random()

    def __process_random(self) -> Queue:
        tracks = get_queue_random(self.config.mount.value, self.config.queue_amount)
        return Queue(
            config=self.config,
            track_list=playlist_paths(tracks),
            tracks=tracks
        )


@dataclass(frozen=True)
class Queue:
    config: Config
    track_list: list[str]
    tracks: list[Track]

    @property
    def total_duration(self) -> int:
        total = 0
        for track in self.tracks:
            duration = track.duration.split(':')
            minutes, seconds = int(duration[0]), int(duration[1])
            total += minutes * 60 + seconds
        return total

    @property
    def amount(self) -> int:
        return len(self.tracks)

    def __str__(self):
        return f'{len(self.track_list)=}'