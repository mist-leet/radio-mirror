from typing import Any
from database.connection import cursor
from database.models import TModel


class CRUD:

    class _Utils:

        @staticmethod
        def _filter_none(data: dict) -> dict:
            return {
                key: value for key, value in data.items()
                if value is not None
            }

        @classmethod
        def __template_value_format(cls, value: Any) -> str:
            if isinstance(value, str):
                value = value.replace("'", "''")
                return f'\'{value}\''
            return value

        @classmethod
        def create_template(cls, table: str, data: dict[str, Any]) -> str:
            filtered_data = cls._filter_none(data)
            template_start = f'INSERT INTO "{table}"'
            template_fields = '(' + ','.join([f'"{field_name}"' for field_name in filtered_data.keys()]) + ')'
            template_values = 'VALUES (' + ','.join([
                f'{cls.__template_value_format(value)}' for value in filtered_data.values()
            ]) + ')'
            template_return = 'RETURNING ' + ','.join([f'"{field_name}"' for field_name in data.keys()])
            return template_start + template_fields + template_values + template_return

        @classmethod
        def find_template(cls, table: str, data: dict[str, Any]) -> str:
            template_start = f'SELECT * FROM "{table}"'
            template_where = 'WHERE ' + ' AND '.join([
                f'"{field_name}" = {cls.__template_value_format(value)}' for field_name, value in data.items()
            ])
            return template_start + template_where

        @classmethod
        def read_template(cls, table: str, data: dict[str, Any]) -> str:
            template_start = f'SELECT * FROM "{table}"'
            template_where = 'WHERE ' + ' AND '.join([
                f'"{field_name}" = {value}' for field_name, value in data.items()
            ])
            return template_start + template_where

        @classmethod
        def list_template(cls, table: str, data: dict[str], amount: int) -> str:
            template_start = f'SELECT * FROM "{table}"'
            template_where = ''
            if data:
                template_where = 'WHERE ' + ' AND '.join([
                    f'"{field_name}" = {cls.__template_value_format(value)}'
                    for field_name, value in data.items()
                ])
            template_limit = f'\nLIMIT {amount}'
            return template_start + template_where + template_limit

    @classmethod
    def find(cls, object: TModel) -> TModel | None:
        template = cls._Utils.find_template(object.table, object.to_dict(filter_none=True))
        cursor.execute(template)
        row = cursor.fetchone()
        col_names = [desc[0] for desc in cursor.description]
        if not row:
            return None
        result = dict(zip(col_names, row))
        return object.from_dict(result)

    @classmethod
    def read(cls, object: TModel) -> TModel | None:
        if object.id is None:
            raise ValueError(f'No "id" field found in {object}')
        template = cls._Utils.read_template(object.table, {'id': object.id})
        cursor.execute(template)
        row = cursor.fetchone()
        if not row:
            return None
        col_names = [desc[0] for desc in cursor.description]
        result = dict(zip(col_names, row))
        return object.from_dict(result)

    @classmethod
    def create(cls, object: TModel) -> TModel:
        template = cls._Utils.create_template(object.table, object.to_dict())
        cursor.execute(template)
        row = cursor.fetchone()
        col_names = [desc[0] for desc in cursor.description]
        result = dict(zip(col_names, row))
        return object.from_dict(result)

    @classmethod
    def list(cls, object: TModel, amount: int = 100) -> list[TModel]:
        template = cls._Utils.list_template(object.table, object.to_dict(filter_none=True), amount)
        cursor.execute(template)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            col_names = [desc[0] for desc in cursor.description]
            result.append(dict(zip(col_names, row)))
        return [object.from_dict(row) for row in result]