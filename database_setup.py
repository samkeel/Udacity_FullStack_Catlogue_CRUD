from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Catalogue(Base):
    __tablename__ = 'catalogue'

    cat_id = Column(Integer, primary_key=True)
    cat_name = Column(String(), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'cat_id': self.cat_id,
            'cat_name': self.cat_name
        }


class Item(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True)
    catalogue_id = Column(Integer, ForeignKey('catalogue.cat_id'))
    userpost_id = Column(Integer, nullable=False)
    movie_title = Column(String(), nullable=False)
    movie_description = Column(String(255), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'item_id': self.item_id,
            'catalogue_id': self.catalogue_id,
            'userpost_id': self.userpost_id,
            'movie_title': self.movie_title,
            'movie_description': self.movie_description
        }


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(), nullable=False)
    email = Column(String(), nullable=False)

engine = create_engine('sqlite:///movies.db')


Base.metadata.create_all(engine)
