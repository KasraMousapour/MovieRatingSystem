from pydantic import BaseModel, Field
from typing import List
from .director_schema import DirectorSchema
from .genre_schema import GenreSchema

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    release_year: int = Field(..., ge=1888, le=2100)
    description: str = Field(..., min_length=1)
    director_id: int = Field(..., ge=1)
    cast: str = Field(..., min_length=1)
    genres: List[int] = Field(..., min_items=1)  # list of genre IDs

class MovieResponse(BaseModel):
    id: int
    title: str
    release_year: int
    description: str
    cast: str
    avg_rating: float
    rating_count: int
    director_id: int
    director: DirectorSchema
    genres: List[int]

    class Config:
        orm_mode = True
