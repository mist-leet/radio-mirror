import json
import os
from typing import Iterator
from dotenv import dotenv_values


class MetaParser:
    # Путь до библиотеки с музыкой
    source_path: str = dotenv_values('radio-console.env').get('MUSIC_VOLUME_PATH')
    meta_file_name = 'meta.json'

    @classmethod
    def update_db(cls):
        for meta_dict in cls.__meta_iter():
            ...

    @classmethod
    def __meta_to_models(cls) -> Iterator:
        ...

    @classmethod
    def __meta_iter(cls) -> Iterator[dict]:
        for path in cls.__source_directory_iter():
            meta_path = os.path.join(path, 'meta.json')
            meta_data = cls.__extract_meta(meta_path)
            if not meta_data:
                print(f'Не удалось загрузить: {meta_path}')
                continue
            yield meta_data

    @classmethod
    def __extract_meta(cls, path: str) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def __source_directory_iter(cls) -> Iterator[str]:
        for root, dirs, files in os.walk(cls.source_path):
            yield from map(lambda dir_name: os.path.join(root, dir_name), dirs)




class ConsoleEngine:
    ...