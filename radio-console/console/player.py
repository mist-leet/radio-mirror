from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from database.models import Track
from console.console import ConsoleEngine
from utils.base import Singleton


class Mount(Enum):

    main = 'main'
    ambient = 'ambient'
    jazz = 'jazz'
    techno = 'techno'

    @classmethod
    def default(cls) -> Mount:
        return Mount.main

    def get(self) -> PlayerMount:
        return PlayerMount(self)


@dataclass
class Queue:

    mount: Mount
    size: int = field(default=100)
    __queue: List[Track] = field(default_factory=list)

    def __update(self):
        self.queue = ConsoleEngine.queue(self.mount, self.size)

    def next(self) -> Track:
        if not self.__queue:
            self.__update()
        return self.__queue.pop()


class PlayerMount(metaclass=Singleton):
    mount: Mount

    __current_track: Track = None
    __queue: Queue = None

    def __init__(self, mount: Mount):
        self.mount = mount
        self.__current_track = None

    def next(self) -> Track:
        self.__current_track = self.__queue.next()
        return self.__current_track

    def set_next(self):
        raise NotImplementedError

    def current(self) -> Track:
        if not self.__current_track:
            self.next()
        return self.__current_track
