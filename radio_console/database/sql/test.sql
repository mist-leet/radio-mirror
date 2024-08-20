INSERT INTO artist (name)
VALUES ('Test Artist') returning id;

INSERT INTO album (name, path, artist_id)
VALUES ('Test', '/www/qwe', 1) returning id;

INSERT INTO track (track_number, artist_id, album_id, genre_id, year, comment, rating, filename, name)
VALUES (1, 1, 1, NULL, 2022, NULL, NULL, '1.mp3', '1'),
       (2, 1, 1, NULL, 2022, NULL, NULL, '2.mp3', '2'),
       (3, 1, 1, NULL, 2022, NULL, NULL, '3.mp3', '3'),
       (4, 1, 1, NULL, 2022, NULL, NULL, '4.mp3', '4'),
       (5, 1, 1, NULL, 2022, NULL, NULL, '5.mp3', '5')
;
