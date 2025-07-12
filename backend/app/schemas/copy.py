from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CaseType(str, Enum):
    unknown = "unknown"
    big_box = "big_box"
    jewel_case = "jewel_case"
    multi_jewel_case = "multi_jewel_case"
    amaray = "amaray"
    dvd_case = "dvd_case"
    sleeve = "sleeve"
    other = "other"

class TagBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    id: int
    file_path: str
    description: Optional[str] = None
    uploaded_at: datetime

    class Config:
        orm_mode = True

class CopyBase(BaseModel):
    id: int
    game_id: int
    sticker_id: Optional[str] = None
    notes: Optional[str] = None

    container_id: Optional[int] = None
    row: Optional[int] = None
    cube: Optional[int] = None
    shelf: Optional[int] = None
    slot: Optional[int] = None
    location_notes: Optional[str] = None

    has_manual: bool = False
    sealed: bool = False
    signed: bool = False
    case_type: CaseType = CaseType.unknown

    date_added: datetime
    date_modified: datetime

    tags: List[TagBase] = []
    images: List[ImageBase] = []

    class Config:
        orm_mode = True

class CopyCreate(BaseModel):
    sticker_id: Optional[str] = None
    notes: Optional[str] = None
    container_id: Optional[int] = None
    row: Optional[int] = None
    cube: Optional[int] = None
    shelf: Optional[int] = None
    slot: Optional[int] = None
    location_notes: Optional[str] = None

    has_manual: bool = False
    sealed: bool = False
    signed: bool = False
    case_type: CaseType = CaseType.unknown

    tag_ids: List[int] = []

class CopyUpdate(CopyCreate):
    pass
