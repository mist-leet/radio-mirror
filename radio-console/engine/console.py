import json
import os
from typing import Iterator, Union, Optional, List
from sqlalchemy import select, func
from database.connection import session
from database.models import Artist, Album, Track
from utils.log import Logger

DB_MODELS = Union[Artist, Album, Track]


class MetaParser:
    # Путь до библиотеки с музыкой
    source_path: str = r'/source'
    meta_file_name = 'meta.json'

    @classmethod
    def run(cls) -> List[str]:
        Logger.info(f'Start parsing meta info')
        result = []
        for meta_dict in cls.__meta_iter():
            print('= ' * 70)
            print(f'Meta: {meta_dict}')
            objects = list(cls.__meta_to_models(meta_dict))
            new_objects = list(filter(lambda x: x.id is None, objects))
            session.add_all(new_objects)
            session.commit()
            result += list(map(str, new_objects))
        return result

    @classmethod
    def __meta_to_models(cls, meta: dict) -> Iterator[DB_MODELS]:
        artist = Artist.get_or_create(name=meta['artist_info']['name'])
        album = Album.get_or_create(name=meta['album_info']['name'], artist=artist, path=meta['album_path'], year=meta['album_info']['year'])
        tracks = [Track.get_or_create(
            name=track['name'],
            track_number=track['track_number'],
            filename=track['filename'],
            artist=artist,
            album=album,
        ) for track in meta['track_list']]
        yield artist
        yield album
        yield from tracks

    @classmethod
    def __meta_iter(cls) -> Iterator[dict]:
        for path in cls.__source_directory_iter():
            meta_path = os.path.join(path, 'meta.json')
            meta_data = cls.__extract_meta(meta_path)
            if not meta_data:
                print(f'Не удалось загрузить: {meta_path}')
                continue
            meta_data['album_path'] = meta_path.replace('/meta.json', '')
            yield meta_data

    @classmethod
    def __extract_meta(cls, path: str) -> Optional[dict]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    @classmethod
    def __source_directory_iter(cls) -> Iterator[str]:
        for root, dirs, files in os.walk(cls.source_path):
            print(root, dirs, files)
            yield from map(lambda dir_name: os.path.join(root, dir_name), dirs)


class ConsoleEngine:

    @classmethod
    def random_track(cls) -> Track:
        query = select(Track).order_by(func.random()).limit(1)
        track: Track = session.scalar(query)
        return track

    @classmethod
    def update_db(cls):
        MetaParser.run()
