from pydantic import BaseModel
from typing import Optional

class GenreSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True