# app/services/movie_service.py
from sqlalchemy.orm import Session
from app.repositories.movie_repository import MovieRepository
from app.models.movie import Movie

class MovieService:
    def __init__(self, session: Session):
        self.session = session
        self.movie_repo = MovieRepository(session)

    def list_movies(self, page: int = 1, page_size: int = 10):
        """
        Return paginated list of movies.
        """
        # calculate offset
        offset = (page - 1) * page_size

        # query movies with limit + offset
        movies_query = self.session.query(Movie).offset(offset).limit(page_size)
        movies = movies_query.all()

        # total count for pagination metadata
        total_count = self.session.query(Movie).count()

        return {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": (total_count + page_size - 1) // page_size,
            "items": movies
        }
