# app/models/copy.py

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db import Base
import datetime
from enum import Enum as PyEnum

from app.models.tag import copy_tags
from app.models.container import Container  # <--- Ensure this is imported here

class CaseType(PyEnum):
    unknown = "unknown"
    big_box = "big_box"
    jewel_case = "jewel_case"
    multi_jewel_case = "multi_jewel_case"
    amaray = "amaray"
    dvd_case = "dvd_case"
    sleeve = "sleeve"
    other = "other"

class Copy(Base):
    __tablename__ = "copies"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    sticker_id = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    container_id = Column(Integer, ForeignKey("containers.id"), nullable=True)
    row = Column(Integer, nullable=True)
    cube = Column(Integer, nullable=True)
    shelf = Column(Integer, nullable=True)
    slot = Column(Integer, nullable=True)
    location_notes = Column(String, nullable=True)

    has_manual = Column(Boolean, default=False)
    sealed = Column(Boolean, default=False)
    signed = Column(Boolean, default=False)
    case_type = Column(Enum(CaseType), default=CaseType.unknown)

    date_added = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    date_modified = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), onupdate=lambda: datetime.datetime.now(datetime.UTC))

    game = relationship("Game", back_populates="copies")
    container = relationship("Container", back_populates="copies")

    tags = relationship(
        "Tag",
        secondary=copy_tags,
        back_populates="copies"
    )
    images = relationship(
        "Image",
        back_populates="copy",
        cascade="all, delete-orphan"
    )
