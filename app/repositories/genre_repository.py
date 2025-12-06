from sqlalchemy.orm import Session
from app.models.genre import Genre
from app.repositories import BaseRepository

class GenreRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def create(self, name, description):
        genre = Genre(name=name, description=description)
        return self.add(genre)

    def update_genre(self, genre_id: int, **kwargs):
        genre = self.get(Genre, genre_id)
        if not genre:
            return None
        return self.update(genre, **kwargs)
