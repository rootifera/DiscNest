from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    igdb_id = Column(Integer, unique=True, index=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    cover_url = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=True)

    series = relationship("Series", back_populates="games")
    genres = relationship("Genre", secondary="game_genres", back_populates="games")
    themes = relationship("Theme", secondary="game_themes", back_populates="games")
    modes = relationship("Mode", secondary="game_modes", back_populates="games")
    perspectives = relationship("Perspective", secondary="game_perspectives", back_populates="games")
    developers = relationship("Company", secondary="game_developers", back_populates="games_developed")
    publishers = relationship("Company", secondary="game_publishers", back_populates="games_published")

    copies = relationship("Copy", back_populates="game", cascade="all, delete-orphan")

    @property
    def release_year(self):
        if self.release_date:
            return self.release_date.year
        return None
