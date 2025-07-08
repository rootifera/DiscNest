from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Top level: bookshelf1, kallax1, CD Tower, etc.
    type = Column(String, nullable=True)   # Extra details, e.g. 'kallax', 'tower', optional
    description = Column(String, nullable=True)

    # Relationship: One container can have many games
    games = relationship("Game", back_populates="container", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Container(name={self.name}, type={self.type})>"
