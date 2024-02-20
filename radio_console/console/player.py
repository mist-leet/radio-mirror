from __future__ import annotations

from dataclasses import dataclass, field
from radio_console.database.models import Track
from radio_console.database.functions import playlist_paths
from radio_console.console.console import ConsoleEngine
from radio_console.console.config import Mount, Mode, Config

_mounts: dict[Mount, PlayerMount] = {}


@dataclass
class PlayerMount:
    mount: Mount
    config: Config

    __default_amount: int = field(default=100, init=False)
    __queue: list[Track] = field(default_factory=list, init=False)

    def __post_init__(self):
        if not self.__queue:
            self.update_queue()

    @classmethod
    def get(cls, mount: Mount | str) -> PlayerMount:
        if isinstance(mount, str):
            mount = Mount(mount)
        if mount not in _mounts:
            raise KeyError(f'No registered mount: {mount}')
        return _mounts[mount]

    @classmethod
    def register(cls, mount: Mount, config: Config):
        _mounts[mount] = cls(mount, config)

    def next(self):
        if not self.__queue:
            self.update_queue()
        self.__queue.pop()

    def update_queue(self, tracks: list[Track] | None = None):
        if not tracks:
            self.__queue = ConsoleEngine.update_queue(self.config, self.__default_amount)
            return
        self.__queue = tracks

    def get_playlist(self) -> list[str]:
        return playlist_paths(self.__queue)


PlayerMount.register(Mount.main, Config(Mode.default))
# PlayerMount.register(Mount.jazz, Config(Mode.album))