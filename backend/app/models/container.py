from sqlalchemy import Column, Integer, String
from app.db import Base

class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) # that's the top level, like bookshelf1, kallax1, CD Tower... etc.
    type = Column(String, nullable=True) # you can add a little more detail, optional.
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Container(name={self.name}, type={self.type})>"
