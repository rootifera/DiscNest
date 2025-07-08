from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base
from app.relationships import game_perspectives

class Perspective(Base):
    __tablename__ = "perspectives"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    games = relationship(
        "Game",
        secondary=game_perspectives,
        back_populates="perspectives"
    )
