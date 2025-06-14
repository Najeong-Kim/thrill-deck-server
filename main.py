from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Tag(BaseModel):
  id: int
  name: str

class Movie(BaseModel):
  id: int
  title: str
  description: str
  rating: int
  image: str
  tags: List[Tag]

tags_raw = [
  {
    "id": 1,
    "name": "Action"
  },
  {
    "id": 2,
    "name": "SF"
  },
  {
    "id": 3,
    "name": "Adventure"
  }
]

class MovieList(BaseModel):
    movies: List[Movie]

movies_raw = [{
  "id": 1,
  "title": "Inception",
  "description": "A movie about dreams within dreams",
  "rating": 5,
  "image": "https://picsum.photos/600/400",
  "tags": [
    {
      "id": 1,
      "name": "Action"
    },
    {
      "id": 2,
      "name": "SF"
    },
    {
      "id": 3,
      "name": "Adventure"
    }
  ]},
  {
  "id": 2,
  "title": "The Matrix",
  "description": "A movie about a man who discovers that he is a computer program",
  "rating": 4,
  "image": "https://picsum.photos/600/400",
  "tags": [
    {
      "id": 1,
      "name": "Action"
    },
    {
      "id": 2,
      "name": "SF"
    },
    {
      "id": 3,
      "name": "Adventure"
    }
  ]},
  {
  "id": 3,
  "title": "Interstellar",
  "description": "A movie about a man who travels through time to save his family",
  "rating": 4,
  "image": "https://picsum.photos/600/400",
  "tags": [
    {
      "id": 2,
      "name": "SF"
    },
    {
      "id": 3,
      "name": "Adventure"
    }
  ]}]
  
movies = [Movie(**data) for data in movies_raw]

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/movies", response_model=MovieList)
async def read_movies():
  results = {"movies": movies}
  return results

@app.get("/movies/{movie_id}", response_model=Movie)
async def read_movie(movie_id: int):
  movie = next((x for x in movies if x.id == movie_id), None)
  if movie:
    return movie
  raise HTTPException(status_code=404, detail="Movie not found")
