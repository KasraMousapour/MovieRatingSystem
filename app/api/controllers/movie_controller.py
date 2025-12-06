# api/controllers/movie_controller.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.movie_service import MovieService
from api.controllers_schemas.movie_schema import MovieResponse

router = APIRouter()

@router.get("/", response_model=dict)
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_db)
):
    service = MovieService(session)
    return service.list_movies(page=page, page_size=page_size)
