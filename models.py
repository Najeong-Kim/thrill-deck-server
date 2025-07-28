from sqlalchemy import Column, Integer, String, Date, Numeric, Text, DateTime, SmallInteger
from sqlalchemy.sql import func
from db import Base

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    original_title = Column(String)
    overview = Column(Text)
    release_date = Column(Date)
    vote_average = Column(Numeric(3, 1))
    vote_count = Column(Integer)
    poster_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EscapeRoom(Base):
    __tablename__ = 'escape_rooms'

    id = Column(Integer, primary_key=True, index=True)
    theme_name = Column(String(100), nullable=False)
    branch_name = Column(String(100), nullable=False)
    difficulty = Column(SmallInteger)
    horror_level = Column(SmallInteger)
    location = Column(String(255), nullable=False)
    poster_image_url = Column(Text)
    play_time = Column(Integer)
    synopsis = Column(Text)
