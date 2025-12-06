from pydantic import BaseModel
from typing import Optional, List
from .director_schema import DirectorSchema
from .genre_schema import GenreSchema

class MovieBase(BaseModel):
    title: str
    release_year: Optional[int] = None
    description: Optional[str] = None
    director_id: Optional[int] = None
    cast: Optional[str] = None
    director: Optional[DirectorSchema]
    genres: List[GenreSchema] = []

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    avg_rating: float
    rating_count: int

    class Config:
        orm_mode = True
