from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException
from repositories import *
from models import *

class MovieService:
    def __init__(self, movie_repo: MovieRepository, director_repo: DirectorRepository, 
                 genre_repo: GenreRepository, movie_genre_repo: MovieGenreRepository, rating_repo: MovieRatingRepository):
        self.movie_repo = movie_repo
        self.director_repo = director_repo
        self.genre_repo = genre_repo
        self.movie_genre_repo = movie_genre_repo
        self.rating_repo = rating_repo

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
        query = self.movie_repo.join_with_genres()

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

            # transform ORM objects into dicts with genre names
        items = [
            {
                "id": m.id,
                "title": m.title,
                "release_year": m.release_year,
                "director": m.director,
                "genres": [mg.genre.name for mg in m.genres],
                "cast": m.cast,
                "average_rating": m.avg_rating,
                "ratings_count": m.rating_count,
            }
            for m in movies
        ]

        return {
            "page": page,
            "page_size": page_size,
            "total_items": total_count,
            "items": items
        }
    
    def get_movie_detail(self, movie_id: int):
        """
        Fetch detailed information about a specific movie.
        Includes director, genres, and rating aggregates.
        """
        movie = self.movie_repo.join_with_director_and_genres().filter(Movie.id == movie_id).first()

        if not movie:
            return None
        
        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": movie.director,
            "genres": [mg.genre.name for mg in movie.genres],
            "cast": movie.cast,
            "average_rating": movie.avg_rating,
            "ratings_count": movie.rating_count,
        }
    
    def create_movie(self, data: dict) -> Movie:
        # 1. Validate director exists
        director = self.director_repo.get(Director, data["director_id"])
        if not director:
            raise ValueError("Invalid director_id")

        # 2. Validate genres exist
        valid_genres = []
        for genre_id in data["genres"]:
            genre = self.genre_repo.get(Genre, genre_id)
            if not genre:
                raise HTTPException(status_code=400, detail=f"Invalid genre_id: {genre_id}")
            valid_genres.append(genre)

        # 3. Create movie
        movie = self.movie_repo.create(
            title=data["title"],
            release_year=data["release_year"],
            description=data["description"],
            director_id=data["director_id"],
            cast=data["cast"],
        )

        # 4. Add movie-genre connections
        for genre in valid_genres:
            self.movie_genre_repo.add_genre_to_movie(movie.id, genre.id)

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": movie.director,
            "genres": [mg.genre.name for mg in movie.genres],
            "cast": movie.cast,
            "average_rating": movie.avg_rating,
            "ratings_count": movie.rating_count,
        }
    
    def update_movie(self, movie_id: int, data: dict) -> Movie:
        # 1. Validate movie exists
        movie = self.movie_repo.get(Movie, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # 2. Validate director exists
        director = self.director_repo.get(Director, data["director_id"])
        if not director:
            raise HTTPException(status_code=400, detail="Invalid director_id")

        # 3. Validate genres
        valid_genres = []
        for genre_id in data["genres"]:
            genre = self.genre_repo.get(Genre, genre_id)
            if not genre:
                raise HTTPException(status_code=400, detail=f"Invalid genre_id: {genre_id}")
            valid_genres.append(genre)

        # 4. Update movie fields
        movie = self.movie_repo.update(
            movie,
            title=data["title"],
            release_year=data["release_year"],
            description=data["description"],
            director_id=data["director_id"],
            cast=data["cast"]
        )

        # 5. Refresh movie_genres links
        self.session.query(MovieGenre).filter(MovieGenre.movie_id == movie.id).delete()
        for genre in valid_genres:
            self.movie_genre_repo.add_genre_to_movie(movie.id, genre.id)

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": movie.director,
            "genres": [mg.genre.name for mg in movie.genres],
            "cast": movie.cast,
            "average_rating": movie.avg_rating,
            "ratings_count": movie.rating_count,
        }

    
    def patch_movie(self, movie_id: int, data: dict) -> Movie:
        # 1. Validate movie exists
        movie = self.movie_repo.get(Movie, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # 2. Validate director if provided
        if data.get("director_id") is not None:
            director = self.director_repo.get(Director, data["director_id"])
            if not director:
                raise HTTPException(status_code=400, detail="Invalid director_id")

        # 3. Validate genres if provided
        if data.get("genres") is not None:
            valid_genres = []
            for genre_id in data["genres"]:
                genre = self.genre_repo.get(Genre, genre_id)
                if not genre:
                    raise HTTPException(status_code=400, detail=f"Invalid genre_id: {genre_id}")
                valid_genres.append(genre)

            # refresh movie_genres links
            self.session.query(MovieGenre).filter(MovieGenre.movie_id == movie.id).delete()
            for genre in valid_genres:
                self.movie_genre_repo.add_genre_to_movie(movie.id, genre.id)

        # 4. Update only provided fields
        movie = self.movie_repo.update(movie, **{k: v for k, v in data.items() if k != "genres"})

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": movie.director,
            "genres": [mg.genre.name for mg in movie.genres],
            "cast": movie.cast,
            "average_rating": movie.avg_rating,
            "ratings_count": movie.rating_count,
        }
    
    def delete_movie(self, movie_id: int) -> bool:
        # 1. Validate movie exists
        movie = self.movie_repo.get(Movie, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # 2. Delete related movie_genres
        self.session.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).delete()

        # 3. Delete related movie_ratings
        self.session.query(MovieRating).filter(MovieRating.movie_id == movie_id).delete()

        # 4. Delete movie itself
        self.movie_repo.delete(movie)

        return True
    
    def submit_rating(self, movie_id: int, score: int):
        # 1. Validate movie exists
        movie = self.movie_repo.get(Movie, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # 2. Validate score range (already enforced by schema, but double-check)
        if score < 1 or score > 10:
            raise HTTPException(status_code=400, detail="Score must be between 1 and 10")

        # 3. Add rating entry
        rating = self.rating_repo.create(movie_id=movie_id, score=score)

        # 4. Update movie aggregates
        self.movie_repo.update_rating_aggregates(movie_id, score)

        return {
            "rating_id": rating.id,
            "movie_id": movie_id,
            "score": score,
            "created_at": rating.created_at
        }
