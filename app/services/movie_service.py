from sqlalchemy.orm import Session, joinedload,
from sqlalchemy import and_
from app.repositories.movie_repository import MovieRepository
from app.models import *

class MovieService:
    def __init__(self, session: Session):
        self.session = session
        self.movie_repo = MovieRepository(session)

    def list_movies(
        self,
        title: str = None,
        director_name: str = None,
        genre_name: str = None,
        release_year: int = None,
        page: int = 1,
        page_size: int = 10
    ):
        """
        Search and filter movies with pagination.
        """
        query = self.session.query(Movie)

        # filter by title (case-insensitive)
        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))

        # filter by director
        if director_name:
            query = query.join(Director).filter(Director.name.ilike(f"%{director_name}%"))

        # filter by genre
        if genre_name:
            query = query.join(MovieGenre).join(Genre).filter(Genre.name.ilike(f"%{genre_name}%"))

        # filter by release year
        if release_year:
            query = query.filter(Movie.release_year == release_year)

        # pagination
        total_count = query.count()
        offset = (page - 1) * page_size
        movies = query.offset(offset).limit(page_size).all()

        return {
            "page": page,
            "page_size": page_size,
            "total_items": total_count,
            "items": movies
        }
    
    def get_movie_detail(self, movie_id: int):
        """
        Fetch detailed information about a specific movie.
        Includes director, genres, and rating aggregates.
        """
        movie = (
            self.session.query(Movie)
            .options(
                joinedload(Movie.director),
                joinedload(Movie.genres).joinedload("genre"),
                joinedload(Movie.ratings)
            )
            .filter(Movie.id == movie_id)
            .first()
        )
        return movie
