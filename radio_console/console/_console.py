from __future__ import annotations
from dataclasses import dataclass

from radio_console.database import Track
from radio_console.database import get_queue_random, playlist_paths
from ._config import Config, QueueMode


@dataclass(frozen=True)
class Console:

    config: Config

    @classmethod
    def get_queue(cls, config: Config) -> Queue:
        return cls(config=config).__process_queue()

    def __process_queue(self) -> Queue:
        if self.config.queue_mode == QueueMode.random:
            return self.__process_random()

    def __process_random(self) -> Queue:
        tracks = get_queue_random(self.config.mount.name, self.config.queue_amount)
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
