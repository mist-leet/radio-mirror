import time
from typing import Optional, Type

from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy_utils import database_exists, create_database


class DatabaseEngine:

    __config = {
        'user': 'postgres',
        'password': 'postgres',
        'host': 'postgres',
        'port': '5432',
        'db': 'radio_console',
    }
    __sleep_step = 2.

    @classmethod
    def create(cls) -> Engine:
        engine = cls.__create(cls.__config['db'])
        if not database_exists(engine.url):
            create_database(engine.url)
        return engine

    @classmethod
    def __create(cls, db_name: str) -> Engine:
        total_sleep = 0
        url = cls.__build_url(db_name)
        while True:
            try:
                return create_engine(url, echo=True)
            except Exception as exc:
                time.sleep(cls.__sleep_step)
                total_sleep += cls.__sleep_step
                if total_sleep > 20.:
                    raise exc

    @classmethod
    def __build_url(cls, db_name: Optional[str] = None) -> str:
        # postgresql+psycopg2://postgres:postgres@postgres:5432/radio_console
        user = cls.__config['user']
        password = cls.__config['password']
        host = cls.__config['host']
        port = cls.__config['port']
        db = db_name or cls.__config['db']
        return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'

    @classmethod
    def create_tables_if_need(cls, engine: Engine, base: Type[DeclarativeBase]):
        base.metadata.create_all(engine)


engine = DatabaseEngine.create()
session = Session(engine, expire_on_commit=False)