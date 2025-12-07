from sqlalchemy.orm import Session
from models.movie_rating import MovieRating
from repositories import BaseRepository

class MovieRatingRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def create(self, movie_id: int, score: int):
        rating = MovieRating(movie_id=movie_id, score=score)
        return self.add(rating)

    def list_by_movie(self, movie_id: int):
        return self.session.query(MovieRating).filter(MovieRating.movie_id == movie_id).all()

    def update_rating(self, rating_id: int, **kwargs):
        rating = self.get(MovieRating, rating_id)
        if not rating:
            return None
        return self.update(rating, **kwargs)
