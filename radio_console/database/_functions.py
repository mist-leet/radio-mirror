from ._connection import cursor
from ._models import Track, Vibe
from ._crud import CRUD


def get_queue_random(mount_name: str, amount: int = 100) -> list[Track]:
    if not mount_name:
        raise KeyError(f'Invalid {mount_name=}')
    vibe_id = CRUD.find(Vibe(name=mount_name)).id
    template = f"""
        SELECT 
            t.id as id, 
            t.name as name, 
            t.track_number as track_number, 
            t.artist_id as artist_id, 
            t.album_id as album_id, 
            t.genre_id as genre_id, 
            t.year as year, 
            t.comment as comment, 
            t.rating as rating, 
            t.filename as filename
        FROM track_vibe tv
        LEFT JOIN track t ON t.id = tv.track_id
        WHERE tv.vibe_id = %s
        ORDER BY random()
        LIMIT %s;
    """
    cursor.execute(template, (vibe_id, amount))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        col_names = [desc[0] for desc in cursor.description]
        result.append(dict(zip(col_names, row)))
    return [Track.from_dict(row) for row in result]


def playlist_paths(tracks: list[Track]) -> list[str]:
    track_ids = [trak.id for trak in tracks]
    if list(filter(lambda value: not value or not isinstance(value, int), track_ids)):
        raise ValueError(f'Передан список треков: {tracks}')
    template = f"""
        SELECT CONCAT(A.path, '/', T.filename) as path
        FROM track T
        INNER JOIN album A ON A.id = T.album_id
        WHERE T.id = ANY (%s::INTEGER[])
    """
    cursor.execute(template, (track_ids,))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        col_names = [desc[0] for desc in cursor.description]
        result.append(dict(zip(col_names, row)))
    return [row['path'] for row in result]
