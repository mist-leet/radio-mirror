from enum import Enum
import requests
from console.player import Mount


class InternalHttpClient:

    class InternalAction(Enum):
        next = 'next'

    internal_url = 'http://ezstream:8888'

    @classmethod
    def next(cls, mount: Mount) -> bool:
        url = cls.build_url(mount, cls.InternalAction.next)
        requests.get(url)
        return True

    @classmethod
    def build_url(cls, mount: Mount, action: InternalAction):
        return f'{cls.internal_url}/{mount.value}/{action.value}'
