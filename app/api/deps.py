"""API dependencies."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import *
from app.services.movie_service import MovieService

def get_movie_repository(db: Session = Depends(get_db)) -> MovieRepository:
    return MovieRepository(db)

def get_director_repository(db: Session = Depends(get_db)) -> DirectorRepository:
    return DirectorRepository(db)

def get_genre_repository(db: Session = Depends(get_db)) -> GenreRepository:
    return GenreRepository(db)

def get_movie_genre_repository(db: Session = Depends(get_db)) -> MovieGenreRepository:
    return MovieGenreRepository(db)

def get_movie_rating_repository(db: Session = Depends(get_db)) -> MovieRatingRepository:
    return MovieRatingRepository(db)

def get_movie_service(movie_repo: MovieRepository = Depends(get_movie_repository), 
                      director_repo: DirectorRepository = Depends(get_director_repository),
                      genre_repo: GenreRepository = Depends(get_genre_repository), 
                      movie_genre_repo: MovieGenreRepository = Depends(get_movie_genre_repository),
                      movie_rating_repo: MovieRatingRepository = Depends(get_movie_rating_repository)) -> MovieService:
    return MovieService(movie_repo=movie_repo, director_repo=director_repo,genre_repo=genre_repo,movie_genre_repo=movie_genre_repo,rating_repo=movie_rating_repo)