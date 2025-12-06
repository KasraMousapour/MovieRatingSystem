from pydantic import BaseModel
from typing import Optional

class MovieBase(BaseModel):
    title: str
    release_year: Optional[int] = None
    description: Optional[str] = None
    director_id: Optional[int] = None
    cast: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    avg_rating: float
    rating_count: int

    class Config:
        orm_mode = True
