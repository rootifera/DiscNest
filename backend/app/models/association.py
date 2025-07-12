from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db import Base

game_genres = Table(
    "game_genres",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)
