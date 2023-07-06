from aiohttp import web
from engine.console import ConsoleEngine
from engine.player import Mount


class RadioConsoleApi:

    class Handlers:

        @classmethod
        async def health_check(cls, request: web.Request) -> web.Response:
            return web.json_response({'is_alive': True})

        @classmethod
        async def track(cls, request: web.Request) -> web.Response:
            str_mount = request.match_info.get('mount', Mount.main.value)
            track = Mount(str_mount).get().current()
            return web.Response(body=track.full_path)

        @classmethod
        async def get_current_track_meta(cls, request: web.Request) -> web.Response:
            return web.json_response({})

        @classmethod
        async def next(cls, request: web.Request) -> web.Response:
            str_mount = request.match_info.get('mount', Mount.main.value)
            mount = Mount(str_mount).get()
            mount.next()
            track = mount.current()
            response = track.as_dict()
            response['path'] = track.full_path
            return web.json_response(response)

        @classmethod
        async def update_db(cls, request: web.Request) -> web.Response:
            result = ConsoleEngine.update_db()
            return web.json_response(result)

    @classmethod
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/health_check', cls.Handlers.health_check),
            web.get('/{mount}/track', cls.Handlers.track),
            web.get('/{mount}/next', cls.Handlers.next),
            web.get('/update_db', cls.Handlers.update_db),
        ])
        web.run_app(app, host='0.0.0.0', port=8080)
