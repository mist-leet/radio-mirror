from aiohttp import web
from console.console import ConsoleEngine
from console.player import Mount
from server.internal_client import InternalHttpClient


class RadioConsoleApi:

    class External:

        @classmethod
        async def health_check(cls, request: web.Request) -> web.Response:
            return web.json_response({'is_alive': True})

        @classmethod
        async def track(cls, request: web.Request) -> web.Response:
            str_mount = request.match_info.get('mount', Mount.main.value)
            track = Mount(str_mount).get().current()
            return web.Response(body=track.as_dict())

    class Internal:

        @classmethod
        async def update_db(cls, request: web.Request) -> web.Response:
            result = ConsoleEngine.update_db()
            return web.json_response(result)

        @classmethod
        async def next(cls, request: web.Request) -> web.Response:
            str_mount = request.match_info.get('mount', Mount.main.value)
            player = Mount(str_mount).get()
            player.next()
            InternalHttpClient.next(player.mount)
            return web.json_response()

        @classmethod
        async def track(cls, request: web.Request) -> web.Response:
            str_mount = request.match_info.get('mount', Mount.main.value)
            track = Mount(str_mount).get().current()
            return web.Response(body=track.full_path)

    @classmethod
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/health_check', cls.External.health_check),
            web.get('/{mount}/track', cls.External.track),

            web.get('/internal/update_db', cls.Internal.update_db),
            web.get('/internal/{mount}/next', cls.Internal.next),
            web.get('/internal/{mount}/track', cls.Internal.track),
        ])
        web.run_app(app, host='0.0.0.0', port=8080)
