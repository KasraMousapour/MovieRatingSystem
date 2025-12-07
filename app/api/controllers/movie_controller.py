# api/controllers/movie_controller.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.movie_service import MovieService
from api.controllers_schemas.movie_schema import MovieResponse, MovieCreate

router = APIRouter()

@router.get("/")
def list_movies(
    title: str = Query(None),
    director_name: str = Query(None),
    genre_name: str = Query(None),
    release_year: int = Query(None),
    min_rating: float = Query(None),
    max_rating: float = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_db)
):
    service = MovieService(session)
    return service.list_movies(
        title=title,
        director_name=director_name,
        genre_name=genre_name,
        release_year=release_year,
        min_rating=min_rating,
        max_rating=max_rating,
        page=page,
        page_size=page_size
    )

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie_detail(movie_id: int, session: Session = Depends(get_db)):
    service = MovieService(session)
    movie = service.get_movie_detail(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=MovieResponse)
def create_movie(payload: MovieCreate, session: Session = Depends(get_db)):
    service = MovieService(session)
    movie = service.create_movie(payload.dict())
    return movie
