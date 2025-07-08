from app.db import engine, Base
from app.models.genre import Genre
from app.models.company import Company
from app.models.theme import Theme
from app.models.mode import Mode
from app.models.perspective import Perspective
from app.models.series import Series
from app.models.game import Game
import app.relationships  # This ensures join tables are registered

def main():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done!")

if __name__ == "__main__":
    main()
