from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base
from app.relationships import game_developers, game_publishers

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    games_developed = relationship(
        "Game",
        secondary=game_developers,
        back_populates="developers"
    )

    games_published = relationship(
        "Game",
        secondary=game_publishers,
        back_populates="publishers"
    )
