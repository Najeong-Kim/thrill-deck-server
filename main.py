from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import date, datetime

from db import Base, engine, SessionLocal
from models import Movie, EscapeRoom
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

class MovieSchema(BaseModel):
    id: int
    tmdb_id: int
    title: str
    original_title: str | None
    overview: str | None
    release_date: date | None
    vote_average: float | None
    vote_count: int | None
    poster_path: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class EscapeRoomSchema(BaseModel):
    id: int
    theme_name: str
    branch_name: str
    difficulty: int | None
    horror_level: int | None
    location: str
    poster_image_url: str | None
    play_time: int | None
    synopsis: str | None

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MovieList(BaseModel):
    movies: List[MovieSchema]

class EscapeRoomList(BaseModel):
    escape_rooms: List[EscapeRoomSchema]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/movies", response_model=MovieList)
async def read_movies(db: Session = Depends(get_db)):
    all_movies = db.query(Movie).all()
    return {"movies": all_movies}

@app.get("/movies/{movie_id}", response_model=MovieSchema)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie:
        return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@app.get("/escape-rooms", response_model=EscapeRoomList)
async def read_escape_rooms(db: Session = Depends(get_db)):
    all_escape_rooms = db.query(EscapeRoom).all()
    return {"escape_rooms": all_escape_rooms}

@app.get("/escape-rooms/{escape_room_id}", response_model=EscapeRoomSchema)
async def read_escape_room(escape_room_id: int, db: Session = Depends(get_db)):
    escape_room = db.query(EscapeRoom).filter(EscapeRoom.id == escape_room_id).first()
    if escape_room:
        return escape_room
    raise HTTPException(status_code=404, detail="Escape room not found")