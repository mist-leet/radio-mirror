from aiohttp import web
from radio_console.console.console import ConsoleEngine
from radio_console.console.player import Mount, PlayerMount
from radio_console.server.internal_client import InternalHttpClient


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
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/health_check', cls.External.health_check),
            # web.get('/{mount}/update', cls.External.update),
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            web.get('/internal/update_db', cls.Internal.update_db),
            web.get('/internal/{mount}/update', cls.Internal.update),
            web.get('/internal/{mount}/next', cls.Internal.next),
        ])
        web.run_app(app, host='0.0.0.0', port=8080)
