# api/controllers/movie_controller.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.services.movie_service import MovieService
from app.repositories import *
from app.api.controllers_schemas.movie_schema import *
from datetime import datetime
from app.api.deps import get_movie_service
import logging
import logging.config
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(BASE_DIR, "config", "logging.conf"), disable_existing_loggers=False)
logger = logging.getLogger("api")

router = APIRouter()

@router.get("")
def list_movies(
    title: str = Query(None),
    director_name: str = Query(None),
    genre_name: str = Query(None),
    release_year: int = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: MovieService = Depends(get_movie_service)
):
    logger.info("List movies called with filters: title=%s, director=%s, genre=%s, year=%s, page=%s, page_size=%s",
                title, director_name, genre_name, release_year, page, page_size)
    
    result = service.list_movies(
        title=title,
        director_name=director_name,
        genre_name=genre_name,
        release_year=release_year,
        page=page,
        page_size=page_size
    )
    logger.debug("List movies returned %d items", len(result["items"]))
    return result

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie_detail(movie_id: int, service: MovieService = Depends(get_movie_service)):
    movie = service.get_movie_detail(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=MovieResponse)
def create_movie(payload: MovieCreate, service: MovieService = Depends(get_movie_service)):
    try:
        movie = service.create_movie(payload.dict())
        return movie
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{movie_id}", response_model=MovieUpdateResponse)
def update_movie(movie_id: int, payload: MovieUpdate, service: MovieService = Depends(get_movie_service)):
    try:
        movie = service.update_movie(movie_id, payload.dict())
        if not movie:
            raise LookupError("Movie not found")
        movie["updated_at"] = datetime.now()
        return movie
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/{movie_id}", response_model=MovieResponse)
def patch_movie(movie_id: int, payload: MoviePatch, service: MovieService = Depends(get_movie_service)):
    try:
        movie = service.patch_movie(movie_id, payload.dict(exclude_unset=True))
        if not movie:
            raise LookupError("Movie not found")
        movie["updated_at"] = datetime.now()
        return movie
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int, service: MovieService = Depends(get_movie_service)):
    try:
        success = service.delete_movie(movie_id)
        if not success:
            raise LookupError("Movie not found")
        return None
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@router.post("/{movie_id}/rating", response_model=MovieRatingResponse)
def rate_movie(movie_id: int, payload: MovieRatingCreate, service: MovieService = Depends(get_movie_service)):
    try:
        logger.info(f"Rating movie(movie_id={movie_id}, rating={payload.dict().get("score")}, route=api/v1/movies/{movie_id}/rating)")
        submit = service.submit_rating(movie_id, payload.score)
        logger.info(f"Rating saved successfully (movie_id={movie_id}, rating={payload.dict().get("score")})")
        return submit
    except LookupError as e:
        logger.error(f"movie {movie_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        logger.warning(f"Invalid rating value (movie_id={movie_id}, rating={payload.dict().get("score")}, route=api/v1/movies/{movie_id}/rating) ")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to save rating (movie_id={movie_id}, rating={payload.dict().get("score")}) ")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

