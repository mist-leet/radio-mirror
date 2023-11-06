from radio_console.database.connection import DatabaseEngine, engine
from radio_console.console.metadata import MetaParser

assert engine is not None

from database.models import Base
DatabaseEngine.create_tables_if_need(engine, Base)
MetaParser.run()
# from server.server import RadioConsoleApi
# RadioConsoleApi.start()