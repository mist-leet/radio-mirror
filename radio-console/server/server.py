from aiohttp import web


class RadioConsoleApi:

    class Handlers:

        # GET

        @classmethod
        async def health_check(cls, request: web.Request) -> web.Response:
            return web.json_response({'is_alive': True})

        @classmethod
        async def get_current_track(cls, request: web.Request) -> web.Response:
            return web.json_response({})

        @classmethod
        async def get_current_track_meta(cls, request: web.Request) -> web.Response:
            return web.json_response({})

        @classmethod
        async def next_track(cls, request: web.Request) -> web.Response:
            return web.json_response({})

        @classmethod
        async def get_playlist(cls, request: web.Request) -> web.Response:
            return web.json_response({})

        # POST

        @classmethod
        async def set_next_tracks(cls, request: web.Request) -> web.Response:
            return web.json_response({})

    @classmethod
    def start(cls):
        app = web.Application()
        app.add_routes([
            web.get('/health_check', cls.Handlers.health_check),
            web.get('/get_current_track', cls.Handlers.get_current_track),
            web.get('/get_current_track_meta', cls.Handlers.get_current_track),
            web.get('/next_track', cls.Handlers.next_track),
            web.get('/get_playlist', cls.Handlers.get_playlist),
            web.post('/set_next_tracks', cls.Handlers.set_next_tracks),
        ])
        web.run_app(app)
