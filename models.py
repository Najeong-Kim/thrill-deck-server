from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from db import Base

movie_tag_table = Table(
    'movie_tag',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    rating = Column(Integer)
    image = Column(String)
    tags = relationship("Tag", secondary=movie_tag_table, back_populates="movies")

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    movies = relationship("Movie", secondary=movie_tag_table, back_populates="tags")
