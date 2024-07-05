def init_db():
    from database.connection import DatabaseEngine, engine
    from database.models import Base
    DatabaseEngine.create_tables_if_need(engine, Base)

