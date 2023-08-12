from database.connection import DatabaseEngine, engine
from metadata import MetaParser

assert engine is not None

from database.models import Base
DatabaseEngine.create_tables_if_need(engine, Base)
MetaParser.run()
# from server.server import RadioConsoleApi
# RadioConsoleApi.start()