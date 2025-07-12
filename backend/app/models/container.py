from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base


class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=True)
    description = Column(String, nullable=True)

    copies = relationship("Copy", back_populates="container", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Container(name={self.name}, type={self.type})>"
