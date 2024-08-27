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
    artist_id INT REFERENCES artist (id)

);


DROP TABLE IF EXISTS vibe CASCADE;
CREATE TABLE IF NOT EXISTS vibe
(
    id   SERIAL PRIMARY KEY,
    name TEXT
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
    filename     TEXT
);

DROP TABLE IF EXISTS track_vibe CASCADE;
CREATE TABLE IF NOT EXISTS track_vibe
(
    id       SERIAL PRIMARY KEY,
    track_id INT REFERENCES track (id),
    vibe_id  INT REFERENCES vibe (id)
);

INSERT INTO vibe (name)

VALUES ('tech'),
       ('ambient'),
       ('sex'),
       ('rus'),
       ('back')
;