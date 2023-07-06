from __future__ import annotations

from enum import Enum, auto
from typing import Union

from database.models import Track
from engine.console import ConsoleEngine
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


class PlayerMount(metaclass=Singleton):
    mount: Mount
    __current_track: Track = None

    def __init__(self, mount: Mount):
        self.mount = mount
        self.__current_track = None

    def next(self):
        self.__current_track = ConsoleEngine.random_track()

    def set_next(self):
        raise NotImplementedError

    def current(self) -> Track:
        if not self.__current_track:
            self.next()
        return self.__current_track
