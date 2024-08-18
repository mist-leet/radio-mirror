from __future__ import annotations

import json
import logging
import os
import subprocess
from enum import Enum
from signal import SIGUSR1, SIGHUP

from aiohttp import web
from xml_creator import XMLCreator
from mount import Mount


class Utils:
    base_path = r'/'
    subprocesses = []

    class Singal(Enum):
        NEXT = 'SIGUSR1'
        UPDATE = 'SIGHUP'

        @property
        def int(self) -> int:
            if self == self.NEXT:
                return SIGUSR1
            if self == self.UPDATE:
                return SIGHUP
            raise ValueError

    @classmethod
    def run_ezstream(cls, mount: Mount):
        logging.info(f'Run EZSTREAM ({mount})')
        XMLCreator.create(mount)
        command = f'/usr/bin/ezstream -v -c /ezstream/ezstream_{mount.value}.xml'
        process = subprocess.Popen(command, shell=True)
        logging.info(f'End.')
        return process

    @classmethod
    def send_signal(cls, mount: Mount, signal: Singal):
        ezstream_pids = cls.__get_pids(mount)
        for pid in ezstream_pids:
            logging.info(f'Sending signal {signal} to {pid} / {ezstream_pids}')
            try:
                subprocess.run(f'kill -s {signal.value.replace("SIG", "")} {pid}', shell=True)
            except Exception as exc:
                logging.error(f'Error during sending signal {exc}')

    @classmethod
    def __get_pids(cls, mount: Mount) -> list[int]:
        process_name = f'ezstream_{mount.value}'
        cmd = "ps aux | grep {}".format(process_name)
        output = subprocess.check_output(cmd, shell=True).decode()
        pid_list = [
            int(line.split()[1])
            for line in output.splitlines()
            if process_name in line
        ]
        return pid_list

    @classmethod
    def write_playlist(cls, mount: Mount, data: list[str]):
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
        async def next(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount', Mount.main.value))
            Utils.send_signal(mount, Utils.Singal.NEXT)
            return web.Response()

        @classmethod
        async def update(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount', Mount.main.value))
            body: str = await request.text()
            body: list[str] = json.loads(body.encode('utf-8'))
            if not body:
                return web.Response(status=200, text='No data')
            if not isinstance(body, list) or not isinstance(body[0], str):
                return web.Response(status=400, text=f'Invalid data, type={type(body)}, type[0]={type(body[0])}')
            logging.info(f'Got {len(body)} tracks for update: {body[0][:30]}...')
            Utils.write_playlist(mount, body)
            Utils.send_signal(mount, Utils.Singal.UPDATE)
            Utils.send_signal(mount, Utils.Singal.NEXT)
            return web.Response()

        @classmethod
        async def create(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount', Mount.main.value))
            Utils.run_ezstream(mount)
            return web.Response()

    @classmethod
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/health_check', cls.__Handlers.health_check),
            web.get('/{mount}/next', cls.__Handlers.next),
            web.post('/{mount}/update', cls.__Handlers.update),
            web.post('/{mount}/create', cls.__Handlers.create),
        ])
        web.run_app(app, host='0.0.0.0', port=8888)


logging.basicConfig(level=logging.DEBUG)
Server.start()
