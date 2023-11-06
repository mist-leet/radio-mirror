from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Union

from radio_console.database.models import Track
from radio_console.console.console import ConsoleEngine


class Mount(Enum):

    main = 'main'
    ambient = 'ambient'
    jazz = 'jazz'
    techno = 'techno'

    @classmethod
    def default(cls) -> Mount:
        return Mount.main

    @classmethod
    def __int_map(cls) -> Dict[Mount, int]:
        return {
            cls.main: 1,
            cls.jazz: 2,
            cls.ambient: 3
        }

    @classmethod
    def __int_rev_map(cls) -> Dict[int, Mount]:
        return {
            1: cls.main,
            2: cls.jazz,
            3: cls.ambient,
        }

    @classmethod
    def from_int(cls, value: int) -> Mount:
        return cls.__int_rev_map().get(value)

    @property
    def int(self) -> int:
        return self.__int_map().get(self)

    @property
    def playlist_name(self):
        return f'playlist_{self.value}.txt'

    def __str__(self):
        return (f'Mount [{self.int}] - {self.name}. file: ezstream_{self.name}.xml')



class Mode(Enum):
    default = 'default'
    album = 'album'


@dataclass(frozen=True)
class Config:
    mode: Mode = field(default=Mode.default)


_mounts: Dict[Mount, PlayerMount] = {}


@dataclass
class PlayerMount:
    mount: Mount
    config: Config

    __default_amount: int = field(default=100, init=False)
    __queue: List[Track] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.__queue = ConsoleEngine.update_queue(self.mount, self.__default_amount)

    @classmethod
    def get(cls, mount: Union[Mount, str]) -> PlayerMount:
        if isinstance(mount, str):
            mount = Mount(mount)
        if mount not in _mounts:
            raise KeyError(f'No registered mount: {mount}')
        return _mounts[mount]

    @classmethod
    def register(cls, mount: Mount, config: Config):
        _mounts[mount] = cls(mount, config)
    
    def all(self) -> List[Track]:
        return self.__queue

    def all_text(self) -> List[str]:
        return [track.full_path for track in self.__queue]

    def update(self):
        self.__queue = ConsoleEngine.update_queue(self.mount, self.__default_amount)


PlayerMount.register(Mount.main, Config(Mode.default))
PlayerMount.register(Mount.jazz, Config(Mode.album))