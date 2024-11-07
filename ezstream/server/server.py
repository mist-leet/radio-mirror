from __future__ import annotations

import json
import logging
from aiohttp import web
from log import Logger
from mount import Mount
from conrotller import EZStreamController


class Server:
    class __Handlers:

        @classmethod
        async def health_check(cls, request: web.Request) -> web.Response:
            return web.json_response({'is_alive': True, 'ezstream': EZStreamController.info()})

        @classmethod
        async def next(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount'))
            EZStreamController(mount).send_next()
            return web.Response()

        @classmethod
        async def init_playlist(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount'))
            body: str = await request.text()
            body: list[str] = json.loads(body.encode('utf-8'))
            if not body:
                return web.Response(status=200, text='No data')
            if not isinstance(body, list) or not isinstance(body[0], str):
                return web.Response(status=400, text=f'Invalid data, type={type(body)}, type[0]={type(body[0])}')
            Logger.info(f'Got {len(body)} tracks for update: {body[0][:30]}...')
            EZStreamController(mount).update_playlist(body)
            return web.Response()

        @classmethod
        async def update(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount'))
            body: str = await request.text()
            body: list[str] = json.loads(body.encode('utf-8'))
            if not body:
                return web.Response(status=200, text='No data')
            if not isinstance(body, list) or not isinstance(body[0], str):
                return web.Response(status=400, text=f'Invalid data, type={type(body)}, type[0]={type(body[0])}')
            Logger.info(f'Got {len(body)} tracks for update: {body[0][:30]}...')
            EZStreamController(mount).update_instance(body)
            return web.Response()

        @classmethod
        async def create(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount'))
            EZStreamController(mount).create_instance()
            return web.json_response({})

    @classmethod
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/health_check', cls.__Handlers.health_check),
            web.get('/{mount}/next', cls.__Handlers.next),
            web.post('/{mount}/update', cls.__Handlers.update),
            web.post('/{mount}/init_playlist', cls.__Handlers.init_playlist),
            web.get('/{mount}/create', cls.__Handlers.create),
        ])
        web.run_app(app, host='0.0.0.0', port=8888)


logging.basicConfig(level=logging.DEBUG)
Server.start()
