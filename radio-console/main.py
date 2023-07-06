from database.connection import DatabaseEngine, engine
assert engine is not None

from database.models import Base
DatabaseEngine.create_tables_if_need(engine, Base)

from server.server import RadioConsoleApi


RadioConsoleApi.start()