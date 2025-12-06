from sqlalchemy import Column, Integer, String, Text
from db.base import Base

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    description = Column(Text)
