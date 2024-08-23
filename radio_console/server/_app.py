from aiohttp import web
import aiohttp_cors

from ._entrypoint import queue_state
from ._internal_client import InternalClient
from radio_console.meta import MetadataParser

class RadioConsoleApi:

    class External:

        @classmethod
        async def health_check(cls, request: web.Request) -> web.Response:
            return web.json_response({'is_alive': True})

        @classmethod
        async def update(cls, request: web.Request) -> web.Response:
            MetadataParser.run()
            return web.json_response({'is_alive': True})

        @classmethod
        async def queue_info(cls, request: web.Request) -> web.Response:
            return web.json_response(queue_state.build_queue_info())

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
            web.get('/health_check', cls.External.health_check),
            web.get('/update', cls.External.update),
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
