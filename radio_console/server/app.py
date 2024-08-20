from aiohttp import web
import aiohttp_cors
from console_old.console_engine import ConsoleEngine
from console_old.player import Mount, PlayerMount
from server.internal_client import InternalHttpClient


class RadioConsoleApi:

    class External:

        @classmethod
        async def health_check(cls, request: web.Request) -> web.Response:
            return web.json_response({'is_alive': True})

    class Internal:

        @classmethod
        async def update(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount', Mount.main.value))
            player = PlayerMount.get(mount)
            player.update_queue()
            playlist_data = player.get_playlist()
            InternalHttpClient.API.update(mount, playlist_data)

        @classmethod
        async def update_db(cls, request: web.Request) -> web.Response:
            result = ConsoleEngine.update_db()
            return web.json_response(result)

        @classmethod
        async def next(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount', Mount.main.value))
            player = PlayerMount.get(mount)
            player.next()
            InternalHttpClient.API.next(mount)
            return web.json_response()

        @classmethod
        async def track(cls, request: web.Request) -> web.Response:
            mount = Mount(request.match_info.get('mount', Mount.main.value))
            player = PlayerMount.get(mount)
            track_name = InternalHttpClient.Icecast.track(mount)
            return web.json_response(player.track_info(track_name))

    @classmethod
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/health_check', cls.External.health_check),
            # web.get('/{mount}/update', cls.External.update),
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            web.get('/internal/update_db', cls.Internal.update_db),
            web.get('/internal/{mount}/update', cls.Internal.update),
            web.get('/internal/{mount}/next', cls.Internal.next),
            web.get('/internal/{mount}/track', cls.Internal.track),
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
