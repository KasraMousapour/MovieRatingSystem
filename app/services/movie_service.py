from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException
from app.repositories import *
from app.models import *

class MovieService:
    def __init__(self, session: Session):
        self.session = session
        self.movie_repo = MovieRepository(session)
        self.director_repo = DirectorRepository(session)
        self.genre_repo = GenreRepository(session)
        self.movie_genre_repo = MovieGenreRepository(session)

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
    
    def create_movie(self, data: dict) -> Movie:
        # 1. Validate director exists
        director = self.director_repo.get(model=self.director_repo.session.query(Movie).mapper.class_, entity_id=data["director_id"])
        director = self.director_repo.session.query(self.director_repo.session.query(Movie).mapper.class_).filter_by(id=data["director_id"]).first()
        if not director:
            raise HTTPException(status_code=400, detail="Invalid director_id")

        # 2. Validate genres exist
        valid_genres = []
        for genre_id in data["genres"]:
            genre = self.genre_repo.get(model=self.genre_repo.session.query(Movie).mapper.class_, entity_id=genre_id)
            genre = self.genre_repo.session.query(self.genre_repo.session.query(Movie).mapper.class_).filter_by(id=genre_id).first()
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

        return movie
    
    def update_movie(self, movie_id: int, data: dict) -> Movie:
        # 1. Validate movie exists
        movie = self.movie_repo.get(Movie, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # 2. Validate director exists
        director = self.director_repo.get(model=self.director_repo.session.query(Movie).mapper.class_, entity_id=data["director_id"])
        director = self.director_repo.session.query(self.director_repo.session.query(Movie).mapper.class_).filter_by(id=data["director_id"]).first()
        if not director:
            raise HTTPException(status_code=400, detail="Invalid director_id")

        # 3. Validate genres
        valid_genres = []
        for genre_id in data["genres"]:
            genre = self.genre_repo.session.query(self.genre_repo.session.query(Movie).mapper.class_).filter_by(id=genre_id).first()
            if not genre:
                raise HTTPException(status_code=400, detail=f"Invalid genre_id: {genre_id}")
            valid_genres.append(genre)

        # 4. Update movie fields
        movie = self.movie_repo.update(movie,
            title=data["title"],
            release_year=data["release_year"],
            description=data["description"],
            duration_minutes=data["duration_minutes"],
            director_id=data["director_id"],
            cast=data["cast"]
        )

        # 5. Refresh movie_genres links
        self.session.query(MovieGenre).filter(MovieGenre.movie_id == movie.id).delete()
        for genre in valid_genres:
            self.movie_genre_repo.add_genre_to_movie(movie.id, genre.id)

        return movie
    
    def patch_movie(self, movie_id: int, data: dict) -> Movie:
        # 1. Validate movie exists
        movie = self.movie_repo.get(Movie, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # 2. Validate director if provided
        if data.get("director_id") is not None:
            director = self.director_repo.session.query(
                self.director_repo.session.query(Movie).mapper.class_
            ).filter_by(id=data["director_id"]).first()
            if not director:
                raise HTTPException(status_code=400, detail="Invalid director_id")

        # 3. Validate genres if provided
        if data.get("genres") is not None:
            valid_genres = []
            for genre_id in data["genres"]:
                genre = self.genre_repo.session.query(
                    self.genre_repo.session.query(Movie).mapper.class_
                ).filter_by(id=genre_id).first()
                if not genre:
                    raise HTTPException(status_code=400, detail=f"Invalid genre_id: {genre_id}")
                valid_genres.append(genre)

            # refresh movie_genres links
            self.session.query(MovieGenre).filter(MovieGenre.movie_id == movie.id).delete()
            for genre in valid_genres:
                self.movie_genre_repo.add_genre_to_movie(movie.id, genre.id)

        # 4. Update only provided fields
        movie = self.movie_repo.update(movie, **{k: v for k, v in data.items() if k != "genres"})

        return movie
    
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
            "movie_rating": rating.id,
            "movie_id": movie_id,
            "score": score,
            "created_at": rating.created_at
        }
