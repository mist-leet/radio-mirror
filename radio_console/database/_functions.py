from utils import Mount, env_config
from ._connection import fetch_all, fetch_one
from ._models import Track


def get_queue_random(mount: str | Mount, amount: int = 100) -> list[Track]:
    mount = Mount.safe_init(mount)
    if not mount:
        raise KeyError(f'Invalid {mount=}')
    template = """
        SELECT 
            track.id as id, 
            track.name as name, 
            track.track_number as track_number, 
            track.artist_id as artist_id, 
            track.album_id as album_id, 
            track.filename as filename, 
            track.duration as duration
        FROM track_mount
        LEFT JOIN track ON track.id = track_mount.track_id
        WHERE track_mount.mount_id = %s
        ORDER BY random()
        LIMIT %s;
    """
    return fetch_all(template, mount.int, amount, cast_model=Track)


def build_track_info(track_id: int, album_id: int) -> list[dict]:
    template = """
    SELECT
        track.id as id,
        track.name as name,
        track.track_number as track_number,
        track.duration as duration,
        album.name as album_name,
        album.year as album_year,
        artist.name as artist_name,
        CASE
            WHEN track.id = %s THEN TRUE
        ELSE FALSE
        END as is_active
    FROM track
    LEFT JOIN album ON track.album_id = album.id
    LEFT JOIN artist ON album.artist_id = artist.id
    WHERE
        track.album_id = %s
    ORDER BY track.track_number;
    """
    return fetch_all(template, track_id, album_id)


def playlist_paths(tracks: list[Track]) -> list[str]:
    track_ids = [trak.id for trak in tracks]
    if list(filter(lambda value: not value or not isinstance(value, int), track_ids)):
        raise ValueError(f'Передан список треков: {tracks}')
    template = f"""
        SELECT CONCAT(album.path, '/', track.filename) as path
        FROM track 
        INNER JOIN album ON album.id = track.album_id
        WHERE track.id = ANY (%s::INTEGER[])
    """
    result = fetch_all(template, track_ids)
    root_path = env_config.get('YANDEX_DISK_PATH')
    return [
        root_path.replace('__source__', row['path']).replace('\\', '/')
        for row in result
    ]


def cover_path(track: Track) -> str:
    template = """
        SELECT album.path as path
        FROM track
        LEFT JOIN album ON album.id = track.album_id
        WHERE track.id = %s
        LIMIT 1;
    """
    path = fetch_one(template, track.id)['path']
    return env_config.get('YANDEX_DISK_PATH').replace('__source__', path).replace('\\', '/')
