from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from db import Base, engine, SessionLocal
from models import Movie, Tag
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

class TagSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class MovieSchema(BaseModel):
    id: int
    title: str
    description: str
    rating: int
    image: str
    tags: List[TagSchema]

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