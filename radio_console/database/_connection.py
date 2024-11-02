import json
import time
import os
from typing import Any

import psycopg2

from utils import classproperty
from utils import Logger
from utils import env_config
from ._models import TModel


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
        cls._init_database(cursor)
        cls._init_mounts()

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
    def _init_mounts(cls):
        from utils import Mount
        template = """
            INSERT INTO mount (id, name)
            SELECT *
            FROM JSON_TO_RECORDSET(%s::json) AS data(
                 id INT,
                 name TEXT
            )
            ON CONFLICT (name) DO NOTHING
            RETURNING *
        """
        data = [{
            'id': mount.int,
            'name': mount.name,
        } for mount in Mount]
        fetch_one(template, to_json(data))

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
        return ['artist', 'album', 'mount', 'track', 'track_mount']

    @classproperty
    def _init_database_template(self) -> str:
        with open(self._init_path, 'r', encoding='utf-8') as f:
            return f.read()


def to_json(data: list | dict) -> str:
    return json.dumps(data, ensure_ascii=False, default=str)


def fetch_one(template: str, *args, cast_model: type[TModel] | None = None) -> dict[str, Any] | TModel:
    try:
        cursor.execute(template, args)
        row = cursor.fetchone()
    except Exception as exc:
        Logger.error(f'Ошибка SQL-запроса:\n{template}\n{args}\n{exc}')
        raise
    col_names = [desc[0] for desc in cursor.description]
    if not row:
        return {}
    if cast_model is not None:
        return cast_model(dict(zip(col_names, row)))
    return dict(zip(col_names, row))


def fetch_all(template: str, *args, cast_model: type[TModel] | None = None) -> list[dict[str, Any]] | list[TModel]:
    try:
        cursor.execute(template, args)
        rows = cursor.fetchall()
    except Exception as exc:
        Logger.error(f'Ошибка SQL-запроса:\n{template}\n{args}')
        raise
    result = []
    for row in rows:
        col_names = [desc[0] for desc in cursor.description]
        result.append(dict(zip(col_names, row)))
    if cast_model is not None:
        return [cast_model(**row) for row in result]
    return result


cursor = DatabaseEngine.create()
DatabaseEngine.after_create(cursor)
