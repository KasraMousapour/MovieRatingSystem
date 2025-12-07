# app/repositories/movie_repository.py
from sqlalchemy.orm import Session
from models import Movie
from repositories import BaseRepository

class MovieRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def create(self, title, release_year, description, director_id, cast):
        movie = Movie(
            title=title,
            release_year=release_year,
            description=description,
            director_id=director_id,
            cast=cast
        )
        return self.add(movie)

    def get_by_title(self, title: str):
        return self.session.query(Movie).filter(Movie.title == title).first()

    def update_movie(self, movie_id: int, **kwargs):
        movie = self.get(Movie, movie_id)
        if not movie:
            return None
        return self.update(movie, **kwargs)

    def update_rating_aggregates(self, movie_id: int, new_score: int):
        movie = self.get(Movie, movie_id)
        if not movie:
            return None
        total_score = movie.avg_rating * movie.rating_count
        movie.rating_count += 1
        movie.avg_rating = (total_score + new_score) / movie.rating_count
        self.session.commit()
        return movie
