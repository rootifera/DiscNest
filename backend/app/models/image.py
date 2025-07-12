from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
import datetime

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    copy_id = Column(Integer, ForeignKey("copies.id"), nullable=False)
    file_path = Column(String, nullable=False) 
    description = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

    copy = relationship("Copy", back_populates="images")
