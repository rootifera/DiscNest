from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageBase(BaseModel):
    id: int
    file_path: str
    description: Optional[str] = None
    uploaded_at: datetime

    class Config:
        orm_mode = True

class ImageCreate(BaseModel):
    file_path: str
    description: Optional[str] = None
