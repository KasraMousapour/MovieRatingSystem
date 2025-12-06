from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    release_year = Column(Integer)
    description = Column(Text)
    director_id = Column(Integer, ForeignKey("directors.id"))
    cast = Column(Text)  

    director = relationship("Director")
    genres = relationship("MovieGenre", back_populates="movie")
    ratings = relationship("MovieRating", back_populates="movie")
