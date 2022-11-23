import eyed3
import os

from models import Album

path = r"D:\Музыка 2\David August - D'ANGELO - 2018 (320 kbps)"

data = list(filter(lambda x: '.mp3' in x, map(lambda x: x.path, [filename for filename in os.scandir(path)])))
print(data)
album = Album.from_files(data)
print(album.to_dict())

# for filename in os.scandir(path):
#     if filename.is_file():
#         print(filename.path)
#         file = eyed3.load(filename.path)
        # print(file.tag)
        # data = {
        #     'Artist': file.tag.artist,
        #     'Title': file.tag.title,
        #     'Album': file.tag.album,
        #     'Year': file.tag.getBestDate(),
        #     'TrackList': None,
        #     'Image': ,
        #     'Comment': 0,
        #     'Duration'
        # }
# Artist
# Title
# Album
# Year
# TrackList
# Image
# Comment


# audiofile = eyed3.load("song.mp3")