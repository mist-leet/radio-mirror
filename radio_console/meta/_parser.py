import json
import os.path

from database import cursor, fetch_all, fetch_one, to_json

__all__ = ('MetadataParser',)

from utils import Mount


class MetadataParser:

    @classmethod
    def run(cls):
        cls.drop_all()
        path = os.path.join(os.path.dirname(__file__), 'meta.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for row in data:
            mount_id = Mount(row['mount']).int
            artist_id = cls.insert_artist(
                title=row['artist']['name']
            )
            album_id = cls.insert_album(
                name=row['album']['name'],
                path=row['album']['path'],
                year=row['album']['year'],
                artist_id=artist_id,
            )
            cls.insert_track(
                track_data=row['track_list'],
                artist_id=artist_id,
                album_id=album_id,
                mount_id=mount_id
            )

    @classmethod
    def build_tree(cls):
        template = """
            SELECT jsonb_object_agg(artist_name, albums) AS result
            FROM (
                SELECT artist_name, jsonb_object_agg(album_name, tracks) AS albums
                FROM (
                    SELECT artist.name AS artist_name,
                           album.name AS album_name,
                           jsonb_agg(track.name) AS tracks
                    FROM artist
                    LEFT JOIN album ON artist.id = album.artist_id
                    LEFT JOIN track ON album.id = track.album_id
                    GROUP BY artist.name, album.name
                    ORDER BY artist.name, album.name
                ) AS album_tracks
                GROUP BY artist_name
            ) AS artist_albums;
        """
        return fetch_one(template)

    @classmethod
    def insert_artist(cls, title: str) -> int:
        template = """
            INSERT INTO artist (name)
            VALUES (%s)
            ON CONFLICT (name) DO UPDATE SET name=excluded.name
            RETURNING id
        """
        return fetch_one(template, title)['id']

    @classmethod
    def insert_album(cls, name: str, year: str, path: str, artist_id: int) -> int:
        template = """
            INSERT INTO album (name, year, path, artist_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name, artist_id) DO UPDATE SET name=excluded.name
            RETURNING id;
        """
        return fetch_one(template, name, year, path, artist_id)['id']

    @classmethod
    def insert_track(cls, track_data: list[dict], artist_id: int, album_id: int, mount_id: int) -> int:
        json_data = [{
            'name': row['name'],
            'track_number': row['track_number'],
            'duration': row['duration'],
            'filename': row['filename'],
            'artist_id': artist_id,
            'album_id': album_id,
        } for row in track_data]
        template = """
            INSERT INTO track (name, track_number, artist_id, album_id, duration, filename)
            SELECT *
            FROM JSON_TO_RECORDSET(%s::json) AS data(
                name TEXT,
                track_number SMALLINT,
                artist_id INT,
                album_id INT,
                duration TEXT,
                filename TEXT
                )
            ON CONFLICT (artist_id, album_id, filename) DO UPDATE SET name=excluded.name
            RETURNING id;
        """
        result = fetch_all(template, to_json(json_data))
        json_data = [{
            'track_id': row['id'],
            'mount_id': mount_id,
        } for row in result]
        template = '''
            INSERT INTO track_mount (track_id, mount_id)
            SELECT *
            FROM json_to_recordset(%s::json) as data(
                track_id INT,
                mount_id INT
            )
            ON CONFLICT (track_id, mount_id) 
            DO NOTHING
            RETURNING *
        '''
        fetch_one(template, to_json(json_data))

    @classmethod
    def drop_all(cls):
        tables = (
            'artist',
            'album',
            'track',
            'track_mount',
        )
        for table in tables:
            template = f"""
                TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;
            """
            cursor.execute(template)
