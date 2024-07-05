from __future__ import annotations

from dataclasses import dataclass, field
from database.models import Track
from database.functions import playlist_paths, build_track_info
from console.console_engine import ConsoleEngine
from console.config import Mount, Mode, Config
from utils.functions import find_cover, to_base64
from utils.log import Logger

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
        playlist = playlist_paths(self.__queue)
        return playlist

    def track_info(self, track_name: str) -> dict:
        track: Track = next(filter(lambda track: track.name in track_name, self.__queue), None)
        if not track:
            Logger.error(f'No track with name: {track_name}')
            Logger.error(f'queue:')
            for i, track in enumerate(self.__queue):
                Logger.error(f'[{i}] {track.name}')
            raise KeyError(f'No track with name: {track_name} in queue {self.mount}')
        track_dict = build_track_info(track.id)
        path = track_dict.pop('album_path')
        covers = find_cover(path)
        if covers:
            track_dict['cover'] = to_base64(covers[0])
        return track_dict


PlayerMount.register(Mount.main, Config(Mode.default))
# PlayerMount.register(Mount.jazz, Config(Mode.album))