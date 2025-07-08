from app.db import SessionLocal

# Import all your models here to ensure SQLAlchemy relationships are fully loaded
from app.models.container import Container
from app.models.game import Game
from app.models.genre import Genre
from app.models.company import Company
from app.models.theme import Theme
from app.models.mode import Mode
from app.models.perspective import Perspective
from app.models.series import Series

def insert_containers():
    session = SessionLocal()
    # Only add containers if none exist (idempotent)
    if session.query(Container).count() == 0:
        containers = [
            Container(name="Kallax 1", type="kallax", description="Main big IKEA shelf"),
            Container(name="CD Tower", type="tower", description="Tall CD rack by the window"),
            Container(name="Box 1", type="box", description="Cardboard storage box"),
        ]
        session.add_all(containers)
        session.commit()
        print("Sample containers added!")
    else:
        print("Containers already exist, skipping insert.")
    session.close()

if __name__ == "__main__":
    insert_containers()
