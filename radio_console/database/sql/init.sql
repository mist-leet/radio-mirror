DROP TABLE IF EXISTS artist CASCADE;
CREATE TABLE IF NOT EXISTS artist
(
    id   SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

DROP TABLE IF EXISTS album CASCADE;
CREATE TABLE IF NOT EXISTS album
(
    id        SERIAL PRIMARY KEY,
    name      TEXT,
    year      INT,
    path      TEXT,
    artist_id INT REFERENCES artist (id),
    UNIQUE (name, artist_id)
);


DROP TABLE IF EXISTS mount CASCADE;
CREATE TABLE IF NOT EXISTS mount
(
    id   SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

DROP TABLE IF EXISTS track CASCADE;
CREATE TABLE IF NOT EXISTS track
(
    id           SERIAL PRIMARY KEY,
    name         TEXT,
    track_number SMALLINT,
    artist_id    INT REFERENCES artist (id),
    album_id     INT REFERENCES album (id),
    duration     TEXT,
    filename     TEXT,
    UNIQUE (artist_id, album_id, filename)
);


DROP TABLE IF EXISTS track_mount CASCADE;
CREATE TABLE IF NOT EXISTS track_mount
(
    id   SERIAL PRIMARY KEY,
    track_id  INT REFERENCES track (id),
    mount_id  INT REFERENCES mount (id),
    UNIQUE (track_id, mount_id)
);

