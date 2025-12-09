from pydantic import BaseModel
from typing import Optional

class DirectorSchema(BaseModel):
    id: int
    name: str
    birth_year: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True