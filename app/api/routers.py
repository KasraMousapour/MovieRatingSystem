# api/routers.py
from fastapi import APIRouter
from api.controllers import movie_controller, director_controller, genre_controller

api_router = APIRouter()
api_router.include_router(movie_controller.router, prefix="/api/v1/movies", tags=["Movies"])


