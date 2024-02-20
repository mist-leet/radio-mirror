from radio_console.database.connection import cursor
from models import Track


def playlist_paths(tracks: list[Track]) -> list[str]:
    if list(filter(lambda value: not value or not isinstance(value, int))):
        raise ValueError(f'Передан список треков: {tracks}')
    track_ids = [trak.id for trak in tracks]
    trak_ids_str = '{value}'.join(track_ids)
    template = f"""
        SELECT CONCAT(A.path, '/', T.filename) as path
        FROM track T
        INNER JOIN album A ON A.id = T.album_id
        WHERE T.id = ANY (ARRAY {trak_ids_str}::INTEGER[])
    """
    cursor.execute(template)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        col_names = [desc[0] for desc in cursor.description]
        result.append(dict(zip(col_names, row)))
    return [row['path'] for row in result]
