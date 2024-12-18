import re
from enum import Enum
import requests
from utils import Logger, Mount


class InternalClient:
    class Icecast:

        base_url = 'http://icecast:8001'
        vclt_url = 'http://icecast:{port}/{mount}.vclt'

        @classmethod
        def track(cls, mount: Mount) -> str:
            url = cls.build_url(mount)
            Logger.info(f'[GET] {url=}')
            response = requests.get(url)
            match = re.search(r'__source__\/.*\/([^\/]+\.mp3)', response.text)
            if not match:
                raise ValueError(f'Can\'t find TITLE in vclt: {response.text}')
            return match.group(1)

        @classmethod
        def stats(cls) -> dict:
            url = f'{cls.base_url}/status-json.xsl'
            Logger.info(f'[GET] {url=}')
            response = requests.get(url)
            return response.json()

        @classmethod
        def build_url(cls, mount: Mount) -> str:
            return cls.vclt_url.format(
                port=f'800{mount.int}',
                mount=f'stream_{mount.value}'
            )

    class EZStream:

        class Action(Enum):
            next = 'next'
            update = 'update'
            init_playlist = 'init_playlist'
            create = 'create'

        url = 'http://ezstream:8888'

        @classmethod
        def next(cls, mount: Mount) -> bool:
            url = cls.build_url(mount, cls.Action.next)
            Logger.info(f'[GET] {url=}')
            requests.get(url)
            return True

        @classmethod
        def create(cls, mount: Mount) -> bool:
            url = cls.build_url(mount, cls.Action.create)
            Logger.info(f'[GET] {url=}')
            response = requests.get(url)
            try:
                Logger.info(f'Response: {response.json()}')
            except Exception:
                Logger.info(response.text)
            return True

        @classmethod
        def update(cls, mount: Mount, data: list[str]) -> bool:
            url = cls.build_url(mount, cls.Action.update)
            Logger.info(f'[POST] {url=}')
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return True
            Logger.error(f'[ERROR] {response.text}')

        @classmethod
        def init_playlist(cls, mount: Mount, data: list[str]) -> bool:
            url = cls.build_url(mount, cls.Action.init_playlist)
            Logger.info(f'[POST] {url=}')
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return True
            Logger.error(f'[ERROR] {response.text}')

        @classmethod
        def build_url(cls, mount: Mount, action: Action):
            return f'{cls.url}/{mount.value}/{action.value}'
