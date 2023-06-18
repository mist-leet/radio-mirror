from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/radio_console", echo=True)
