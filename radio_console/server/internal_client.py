from enum import Enum
from typing import List

import requests
from radio_console.console.player import Mount


class InternalHttpClient:

    class Icecast:

        url = 'http://icecast:{port}/{mount}.vclt'

        @classmethod
        def status(cls, mount: Mount):
            ...

        @classmethod
        def build_url(cls, mount: Mount) -> str:
            return cls.url.format(
                port=f'000{mount.int}',
                mount=f'stream_{mount.value}'
            )

    class API:

        class Action(Enum):
            next = 'next'
            update = 'update'

        url = 'http://ezstream:8888'

        @classmethod
        def next(cls, mount: Mount) -> bool:
            url = cls.build_url(mount, cls.Action.next)
            requests.get(url)
            return True

        @classmethod
        def update(cls, mount: Mount, data: List[str]) -> bool:
            url = cls.build_url(mount, cls.Action.update)
            requests.post(url, data)
            return True

        @classmethod
        def build_url(cls, mount: Mount, action: Action):
            return f'{cls.url}/{mount.value}/{action.value}'
