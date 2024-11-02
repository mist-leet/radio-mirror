import time
from dataclasses import dataclass, field
from datetime import timedelta

from database import Track
from meta import MetadataParser
from utils import Mount, Logger
from console import Config, Console, QueueMode, Scheduler, Queue
from ._internal_client import InternalClient


class EntryPoint:
    configuration = {
        Config(QueueMode.random, Mount.tech, queue_amount=100),
        Config(QueueMode.random, Mount.ambient, queue_amount=10),
    }

    @classmethod
    def start(cls):
        MetadataParser.run()
        Logger.info('Create EZSTREAMs')
        for config in cls.configuration:
            InternalClient.EZStream.create(config.mount)
            update_one(config)
            time.sleep(2)


def update_one(config: Config):
    Logger.info(f'Update function: {config=}')
    queue = Console.get_queue(config)
    mount = queue.config.mount
    track_list = queue.track_list
    InternalClient.EZStream.update(mount, track_list)
    next_update_delay = timedelta(seconds=queue.total_duration)
    queue_state.update(mount, queue)
    # Scheduler.create(execute_after=next_update_delay,
    #                  function=update_one,
    #                  args=(config,),
    #                  description=f'Scheduler ({mount.name}) for queue {queue.amount}, {queue.total_duration=}')


@dataclass
class QueueState:
    _configuration: dict[Mount, Queue] = field(default_factory=dict, init=False)
    _track_buffer: dict[Mount, Track] = field(default_factory=dict, init=False)

    def update(self, mount: Mount, queue: Queue):
        self._configuration[mount] = queue

    def build_queue_info(self) -> dict:
        result = {}
        for mount, queue in self._configuration.items():
            result[mount.name] = {
                'queue_size': queue.amount,
                'queue_config': str(queue.config),
                'queue': str(queue.track_list[:3]),
            }
        return result

    def build_track_info(self, mount: Mount) -> dict:
        queue = self._configuration[mount]
        track_file_name = InternalClient.Icecast.track(mount)
        track = next(filter(lambda track: track.filename == track_file_name, queue.tracks), None)
        if track is None:
            raise KeyError(f'Не найден {track_file_name=} в очереди {mount}, {queue=}')
        self._update_current_track(mount, track)
        return Console.track_data(track)

    def cover_path(self, mount: Mount) -> str:
        return Console.cover(self.current_track(mount))

    def _update_current_track(self, mount: Mount, track: Track):
        self._track_buffer[mount] = track

    def current_track(self, mount: Mount) -> Track:
        return self._track_buffer[mount]


queue_state = QueueState()
EntryPoint.start()
