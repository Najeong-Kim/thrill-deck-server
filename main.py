from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Movie(BaseModel):
  id: int
  name: str
  thumbnail: str

movies_raw = [{
  "id": 1,
  "name": "Inception",
  "thumbnail": "https://example.com/thumbnails/inception.jpg"
},
{
  "id": 2,
  "name": "The Matrix",
  "thumbnail": "https://example.com/thumbnails/matrix.jpg"
},
{
  "id": 3,
  "name": "Interstellar",
  "thumbnail": "https://example.com/thumbnails/interstellar.jpg"
}]

movies = [Movie(**data) for data in movies_raw]

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/movies", response_model=List[Movie])
async def read_movies():
  results = {"movies": movies}
  return results

@app.get("/movies/{movie_id}", response_model=Movie)
async def read_movie(movie_id: int):
  movie = next((x for x in movies if x.id == movie_id), None)
  if movie:
    return movie
  raise HTTPException(status_code=404, detail="Movie not found")
