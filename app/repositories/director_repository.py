from sqlalchemy.orm import Session
from app.models.director import Director
from app.repositories import BaseRepository

class DirectorRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def create(self, name, birth_year, description):
        director = Director(name=name, birth_year=birth_year, description=description)
        return self.add(director)

    def update_director(self, director_id: int, **kwargs):
        director = self.get(Director, director_id)
        if not director:
            return None
        return self.update(director, **kwargs)
