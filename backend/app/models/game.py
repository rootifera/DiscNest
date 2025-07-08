from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from app.relationships import (
    game_genres,
    game_developers,
    game_publishers,
    game_themes,
    game_modes,
    game_perspectives,
)

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    igdb_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    cover_url = Column(String)
    release_date = Column(Date)
    summary = Column(Text)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=True)

    # New location fields
    container_id = Column(Integer, ForeignKey("containers.id"), nullable=True)
    container = relationship("Container", back_populates="games")
    row = Column(Integer, nullable=True)       # let's assume this is an IKEA Kallax, 5x5, this is the row of cubes
    cube = Column(Integer, nullable=True)     # for the same kallax, this is for each cube
    shelf = Column(Integer, nullable=True)    # if it's more like a bookshelf, then this one is a better option
    slot = Column(Integer, nullable=True)     # this is the exact location of the item. "3" would be the 3rd game from the left etc.
    location_notes = Column(String, nullable=True)  # notes. yeah, just notes. that's it.

    genres = relationship(
        "Genre",
        secondary=game_genres,
        back_populates="games"
    )
    developers = relationship(
        "Company",
        secondary=game_developers,
        back_populates="developed_games"
    )
    publishers = relationship(
        "Company",
        secondary=game_publishers,
        back_populates="published_games"
    )
    themes = relationship(
        "Theme",
        secondary=game_themes,
        back_populates="games"
    )
    modes = relationship(
        "Mode",
        secondary=game_modes,
        back_populates="games"
    )
    perspectives = relationship(
        "Perspective",
        secondary=game_perspectives,
        back_populates="games"
    )
    series = relationship(
        "Series",
        back_populates="games"
    )
