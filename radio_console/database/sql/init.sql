drop table if exists artist cascade;
create table if not exists artist
(
    id   serial primary key,
    name text unique
);

drop table if exists album cascade;
create table if not exists album
(
    id        serial primary key,
    name      text,
    year      int,
    path      text,
    artist_id int references artist (id)

);

drop table if exists genre cascade;
create table if not exists genre
(
    id   serial primary key,
    name text
);

drop table if exists vibe cascade;
create table if not exists vibe
(
    id   serial primary key,
    name text
);

drop table if exists track cascade;
create table if not exists track
(
    id           serial primary key,
    name         text,
    track_number smallint,
    artist_id    int references artist (id),
    album_id     int references album (id),
    genre_id     int references genre (id),
    year         int,
    comment      text,
    rating       smallint,
    filename     text
);

drop table if exists track_vibe cascade;
create table if not exists track_vibe
(
    id       serial primary key,
    track_id int references track (id),
    vibe_id  int references vibe (id)
)