from __future__ import annotations

import logging
import os
import subprocess
from enum import Enum
from typing import List, Dict

from aiohttp import web

from xml_creator import XMLCreator
from mount import Mount

class _PIDMap:

    __map: Dict[int, PID] = None

    def __init__(self):
        self.__map = {}

    def add(self, mount: int, pid: PID):
        self.__map[mount] = pid

    def get(self, mount: int) -> PID:
        return self.__map.get(mount)


PID = int
PIDMap = _PIDMap()


class Utils:
    base_path = r'/'
    subprocesses = []

    class Singal(Enum):
        NEXT = 'USR1'
        UPDATE = 'USR1'

    @classmethod
    def craete_and_run(cls):
        for i in (1, 2):
            XMLCreator.create(i)
            ezstream_pid = cls.run_ezstream(i)
            PIDMap.add(i, ezstream_pid)

    @classmethod
    def run_ezstream(cls, config_number: int) -> PID:
        mount = Mount.from_int(config_number)
        logging.info(f'Run EZSTREAM ({mount}) instance #{config_number}.')
        command = f'/usr/bin/ezstream -v -c /ezstream/ezstream_{mount.value}.xml'
        # result = subprocess.call(command, capture_output=True, shell=True)
        process = subprocess.Popen(command, shell=True)
        # process.wait()
        logging.info(f'End.')
        return 0
        # errors = result.stderr.decode()
        # if errors:
        #     raise Exception(f'Fail to start ezstream:\n{mount}\n{errors}')
        # pid = result.stdout.decode()
        # logging.info(f'*-' * 50)
        # return pid

    @classmethod
    def send_signal(cls, mount: Mount, signal: Singal):
        pid = PIDMap.get(mount.int)
        subprocess.run(f"pkill -{signal.value} {pid}", shell=True, check=True)

    @classmethod
    def write_playlist(cls, mount: Mount, data: List[str]):
        path = os.path.join(cls.base_path, 'ezstream', mount.playlist_name)
        with open(path, 'w', encoding='utf-8') as f:
            for line in data:
                f.write(f'{line}\n')


class Server:
    class __Handlers:

        @classmethod
        async def health_check(cls, request: web.Request) -> web.Response:
            return web.json_response({'is_alive': True})

        @classmethod
        async def create_and_run(cls, request: web.Request) -> web.Response:
            Utils.craete_and_run()
            return web.Response()

        @classmethod
        async def next(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount', Mount.main.value))
            Utils.send_signal(mount, Utils.Singal.NEXT)
            return web.Response()

        @classmethod
        async def update(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount', Mount.main.value))
            body: List[str] = await request.json()
            Utils.write_playlist(mount, body)
            Utils.send_signal(mount, Utils.Singal.UPDATE)
            return web.Response()

    @classmethod
    def test(cls):
        Utils.craete_and_run()

    @classmethod
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/health_check', cls.__Handlers.health_check),
            web.get('/internal/create_and_run', cls.__Handlers.create_and_run),
            web.get('/internal/{mount}/next', cls.__Handlers.next),
            web.post('/internal/{mount}/update', cls.__Handlers.update),
        ])
        web.run_app(app, host='0.0.0.0', port=8888)

logging.basicConfig(level=logging.DEBUG)
Server.start()
# Server.test()
