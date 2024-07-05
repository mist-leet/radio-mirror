from database.connection import cursor
from database.models import Track


def playlist_paths(tracks: list[Track]) -> list[str]:
    track_ids = [trak.id for trak in tracks]
    if list(filter(lambda value: not value or not isinstance(value, int), track_ids)):
        raise ValueError(f'Передан список треков: {tracks}')
    trak_ids_str = ', '.join(map(str, track_ids))
    template = f"""
        SELECT CONCAT(A.path, '/', T.filename) as path
        FROM track T
        INNER JOIN album A ON A.id = T.album_id
        WHERE T.id = ANY (ARRAY [{trak_ids_str}]::INTEGER[])
    """
    cursor.execute(template)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        col_names = [desc[0] for desc in cursor.description]
        result.append(dict(zip(col_names, row)))
    return [row['path'] for row in result]


def build_track_info(track_id: int) -> dict[str, str]:
    if not track_id or not isinstance(track_id, int):
        raise KeyError(f'Invalid track id: {track_id}')
    template = f"""
        SELECT
            track.id as track_id,
            track.name as track_name,
            track.track_number as track_number,
            artist.name as artist_name,
            album.name as album_name,
            album.year as album_year,
            album.path as album_path
        FROM track
                 LEFT JOIN artist ON artist.id = track.artist_id
                 LEFT JOIN album ON album.id = track.album_id
        WHERE track.id = {track_id}
        LIMIT 1;
    """
    cursor.execute(template)
    row = cursor.fetchone()
    col_names = [desc[0] for desc in cursor.description]
    return dict(zip(col_names, row))
