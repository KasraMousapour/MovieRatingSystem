# app/repositories/movie_genre_repository.py
from sqlalchemy.orm import Session
from models.movie_genre import MovieGenre
from repositories import BaseRepository

class MovieGenreRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def add_genre_to_movie(self, movie_id: int, genre_id: int):
        mg = MovieGenre(movie_id=movie_id, genre_id=genre_id)
        return self.add(mg)

    def update_movie_genre(self, movie_id: int, genre_id: int, **kwargs):
        mg = self.session.query(MovieGenre).filter(
            MovieGenre.movie_id == movie_id,
            MovieGenre.genre_id == genre_id
        ).first()
        if not mg:
            return None
        return self.update(mg, **kwargs)
