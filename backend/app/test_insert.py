from app.db import SessionLocal
from app.models.genre import Genre
from app.models.company import Company
from app.models.theme import Theme
from app.models.mode import Mode
from app.models.perspective import Perspective
from app.models.series import Series
from app.models.game import Game

def main():
    session = SessionLocal()

    # Create instances
    genre = Genre(name="Shooter")
    company = Company(name="id Software")
    theme = Theme(name="Action")
    mode = Mode(name="Single Player")
    perspective = Perspective(name="First Person")
    series = Series(name="Quake Series")

    session.add_all([genre, company, theme, mode, perspective, series])
    session.commit()

    # Create and add a game
    game = Game(
        igdb_id=123456,
        name="Quake",
        cover_url="https://example.com/quake.jpg",
        summary="A classic FPS.",
        genres=[genre],
        developers=[company],
        themes=[theme],
        modes=[mode],
        perspectives=[perspective],
        series=series
    )

    session.add(game)
    session.commit()

    print(f"Added game: {game.name} with genre {genre.name}, developer {company.name}, theme {theme.name}, mode {mode.name}, perspective {perspective.name}, series {series.name}")

    session.close()

if __name__ == "__main__":
    main()
