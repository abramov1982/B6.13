# Импорт модулей

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Импорт модулей

DB_PATH = 'sqlite:///albums.sqlite3'
Base = declarative_base()


# Создание классов ошибок и описание структуры базы

class Error(Exception):
    pass

class AlreadyExists(Error):
    pass


class Album(Base):
    __tablename__ = 'album'

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


# Функция соединения с базой данных

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


# Функция поиска альбомов

def find(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


# Функция добавления записей в базу

def save(year, artist, genre, album):
    assert isinstance(year, int), 'Incorrect date'
    assert isinstance(artist, str), 'Incorrect artist'
    assert isinstance(genre, str), 'Incorrect genre'
    assert isinstance(album, str), 'Incorrect album'

    session = connect_db()
    saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_album is not None:
        raise AlreadyExists('Album already exists and has #{}'.format(saved_album.id))

    album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    session.add(album)
    session.commit()
    return album