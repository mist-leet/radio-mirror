from dataclasses import dataclass
from radio_console.database import get_queue_random, playlist_paths
from ._config import Config, QueueMode


@dataclass(frozen=True)
class Console:

    config: Config

    @classmethod
    def get_queue(cls, config: Config) -> list[str]:
        return cls(config=config).__process_queue()

    def __process_queue(self) -> list[str]:
        if self.config.queue_mode == QueueMode.random:
            return self.__process_random()

    def __process_random(self) -> list[str]:
        tracks = get_queue_random(self.config.mount.name, self.config.queue_amount)
        return playlist_paths(tracks)

    def __process_album(self):
        """soon"""