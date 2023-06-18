from sqlalchemy.orm import Session

# from server.server import RadioConsoleApi

# if __name__ == '__main__':
#     RadioConsoleApi.start()
from sqlalchemy import select
from database.connection import engine
from database.models import *

session = Session(engine)

select_query = select(Artist)

artist: Artist = list(session.scalars(select_query))[0]
print(artist.name)
print(artist.tracks)