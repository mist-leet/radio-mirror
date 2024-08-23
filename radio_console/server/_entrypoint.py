from datetime import timedelta
from radio_console.utils import Mount
from radio_console.console import Config, Console, QueueMode, Scheduler, Queue
from ._internal_client import InternalClient


class EntryPoint:
    configuration = {
        Config(QueueMode.random, Mount.tech, queue_amount=100),
        Config(QueueMode.random, Mount.ambient, queue_amount=100),
    }

    @classmethod
    def start(cls):
        for config in cls.configuration:
            update_one(config)


def update_one(config: Config):
    queue = Console.get_queue(config)
    mount = queue.config.mount
    track_list = queue.track_list
    InternalClient.EZStream.update(mount, track_list)
    next_update_delay = timedelta(seconds=queue.total_duration)
    queue_state.update(mount, queue)
    Scheduler.create(execute_after=next_update_delay,
                     function=update_one,
                     args=(config,))


class QueueState:
    _configuration: dict[Mount, Queue]

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


queue_state = QueueState()
