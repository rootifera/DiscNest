from sqlalchemy import Table, Column, Integer, ForeignKey
from .db import Base

game_genres = Table(
    "game_genres",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id")),
    Column("genre_id", Integer, ForeignKey("genres.id"))
)

game_developers = Table(
    "game_developers",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id")),
    Column("company_id", Integer, ForeignKey("companies.id"))
)

game_publishers = Table(
    "game_publishers",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id")),
    Column("company_id", Integer, ForeignKey("companies.id"))
)

game_themes = Table(
    "game_themes",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id")),
    Column("theme_id", Integer, ForeignKey("themes.id"))
)

game_modes = Table(
    "game_modes",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id")),
    Column("mode_id", Integer, ForeignKey("modes.id"))
)

game_perspectives = Table(
    "game_perspectives",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id")),
    Column("perspective_id", Integer, ForeignKey("perspectives.id"))
)