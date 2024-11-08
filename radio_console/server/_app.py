import re
from pathlib import Path

from aiohttp import web
import aiohttp_cors

from frontend import render_html_template
from utils import Logger, Mount
from ._entrypoint import queue_state, EntryPoint
from ._internal_client import InternalClient
from meta import MetadataParser


class RadioConsoleApi:
    __static_path = r'/radio_console/frontend/site'

    class Frontend:

        @classmethod
        async def home(cls, request: web.Request) -> web.Response:
            Logger.info(f'{request.raw_path=}')
            mount = Mount.from_url(request.raw_path)
            content = render_html_template(mount)
            return web.Response(text=content, content_type='text/html')

    class External:

        @classmethod
        async def health_check(cls, request: web.Request) -> web.Response:
            return web.json_response({'is_alive': True})

        @classmethod
        async def update(cls, request: web.Request) -> web.Response:
            log = MetadataParser.run()
            return web.json_response(log)

        @classmethod
        async def next(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount'))
            InternalClient.EZStream.next(mount)
            return web.json_response()

        @classmethod
        async def queue(cls, request: web.Request) -> web.Response:
            return web.json_response(queue_state.build_queue_info())

        @classmethod
        async def track(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount'))
            return web.json_response(queue_state.build_track_info(mount))

        @classmethod
        async def cover(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount'))
            image_path = Path(queue_state.cover_path(mount))
            image_data = image_path.read_bytes()
            return web.Response(body=image_data, content_type="image/jpeg")

        @classmethod
        async def start(cls, request: web.Request) -> web.Response:
            EntryPoint.start()
            return web.json_response({})

        @classmethod
        async def restart(cls, request: web.Request) -> web.Response:

            return web.json_response({})

    class Internal:

        @classmethod
        async def update_db(cls, request: web.Request) -> web.Response:
            ...

        @classmethod
        async def next(cls, request: web.Request) -> web.Response:
            return web.json_response()

        @classmethod
        async def track(cls, request: web.Request) -> web.Response:
            ...

    @classmethod
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/', cls.Frontend.home),
            web.get('/home', cls.Frontend.home),
            web.get('/health_check', cls.External.health_check),
            web.get('/update', cls.External.update),
            web.get('/start', cls.External.start),
            web.get('/restart', cls.External.start),

            web.get('/{mount}/queue', cls.External.queue),
            web.get('/{mount}/track', cls.External.track),
            web.get('/{mount}/cover', cls.External.cover),
            web.get('/{mount}/next', cls.External.next),

            web.static('/static/', cls.__static_path)
        ] + [
            web.get(f'/{mount.value}', cls.Frontend.home)
            for mount in Mount
        ])
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*"
            )
        })

        for route in list(app.router.routes()):
            cors.add(route)
        web.run_app(app, host='0.0.0.0', port=8080)
