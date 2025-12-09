from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
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
    director: DirectorSchema
    genres: List[str]
    cast: str
    average_rating: float
    ratings_count: int

    class Config:
        from_attributes = True

class MovieUpdate(MovieCreate):
    pass

class MovieUpdateResponse(MovieResponse):
    updated_at: datetime

class MoviePatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    release_year: Optional[int] = Field(None, ge=1888, le=2100)
    description: Optional[str] = Field(None, min_length=1)
    duration_minutes: Optional[int] = Field(None, ge=1)
    director_id: Optional[int] = Field(None, ge=1)
    cast: Optional[str] = Field(None, min_length=1)
    genres: Optional[List[int]] = Field(None, min_items=1)    

class MovieRatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=10)  # must be between 1 and 10

class MovieRatingResponse(BaseModel):
    rating_id: int
    movie_id: int
    score: int
    created_at:datetime
       

    class Config:
        from_attributes = True