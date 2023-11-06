def init_db():
    from radio_console.database.connection import DatabaseEngine, engine
    from radio_console.database.models import Base
    DatabaseEngine.create_tables_if_need(engine, Base)

