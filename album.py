import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Описание подключения к базе данных
DB_PATH = 'sqlite:///albums.sqlite3'
Base = declarative_base()

# Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

session = connect_db()

# Описание структуры таблиц в базе данных.
class Album(Base):
    __tablename__ = 'album'

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def find(artist):
    albums = session.query(Album).filter(Album.artist == artist).all()
    if len(albums) == 0:
        return False
    return albums

def add(year, artist, genre, album):
    assert isinstance(year, int), 'Incorrect date'
    assert isinstance(artist, str), 'Incorrect artist'
    assert isinstance(genre, str), 'Incorrect genre'
    assert isinstance(album, str), 'Incorrect album'

    session = connect_db()
    album_add = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if album_add is not None:
        raise AlreadyExists('Такой альбом уже есть и его имя: #{}'.format(saved_album.id))

    album: Album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )    
    session.add(album)
    session.commit()
    return album