from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

copy_tags = Table(
    "copy_tags",
    Base.metadata,
    Column("copy_id", Integer, ForeignKey("copies.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    copies = relationship(
        "Copy",
        secondary=copy_tags,
        back_populates="tags"
    )
