from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base
from app.relationships import game_modes

class Mode(Base):
    __tablename__ = "modes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    games = relationship(
        "Game",
        secondary=game_modes,
        back_populates="modes"
    )
