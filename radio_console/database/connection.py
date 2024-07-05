import time
import os
import psycopg2
from utils.base import classproperty
from utils.log import Logger
from utils.env import env_config


class DatabaseEngine:
    __config = {
        'database': env_config.get('POSTGRES_DB'),
        'user': env_config.get('POSTGRES_USER'),
        'password': env_config.get('POSTGRES_PASSWORD'),
        'host': env_config.get('POSTGRES_HOST'),
        'port': env_config.get('POSTGRES_PORT'),
    }
    _init_path = os.path.join(os.path.dirname(__file__), 'sql/init.sql')
    __sleep_step = 2.

    @classmethod
    def create(cls):
        sleep_counter = 0
        try:
            return cls.__create()
        except Exception as exc:
            if sleep_counter > 10:
                raise exc
            time.sleep(cls.__sleep_step)
            Logger.error(exc)
            Logger.error(f'Wait for db')
            sleep_counter += 1

    @classmethod
    def after_create(cls, cursor):
        if not cls.__check_tables(cursor):
            cls._init_database(cursor)

    @classmethod
    def __create(cls):
        Logger.info(f'Connect database: {cls.__config}')
        conn = psycopg2.connect(**cls.__config)
        conn.autocommit = True
        cursor = conn.cursor()
        return cursor

    @classmethod
    def __build_url(cls, db_name: str | None = None) -> str:
        """postgresql+psycopg2://postgres:postgres@postgres:5432/radio_console"""
        user = cls.__config['user']
        password = cls.__config['password']
        host = cls.__config['host']
        port = cls.__config['port']
        db = db_name or cls.__config['db']
        return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'

    @classmethod
    def _init_database(cls, cursor):
        cursor.execute(cls._init_database_template)

    @classmethod
    def __check_tables(cls, cursor) -> bool:
        base_template = 'SELECT 1 FROM "TABLE";'
        for table in cls._table_list:
            template = base_template.replace('TABLE', table)
            try:
                cursor.execute(template)
            except Exception as exc:
                return False
        return True

    @classproperty
    def _table_list(self) -> list[str]:
        return ['artist', 'album', 'genre', 'vibe', 'track', 'track_vibe']

    @classproperty
    def _init_database_template(self) -> str:
        with open(self._init_path, 'r', encoding='utf-8') as f:
            return f.read()


cursor = DatabaseEngine.create()
DatabaseEngine.after_create(cursor)
