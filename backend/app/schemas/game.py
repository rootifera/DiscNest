from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class CompanySimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class GenreSimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ThemeSimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ModeSimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class PerspectiveSimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class SeriesSimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class GameBase(BaseModel):
    id: int
    igdb_id: Optional[int]
    name: str
    cover_url: Optional[str]
    release_year: Optional[int]

    class Config:
        orm_mode = True

class GameDetail(GameBase):
    summary: Optional[str]
    release_date: Optional[date]
    genres: List[GenreSimple] = []
    themes: List[ThemeSimple] = []
    modes: List[ModeSimple] = []
    perspectives: List[PerspectiveSimple] = []
    developers: List[CompanySimple] = []
    publishers: List[CompanySimple] = []
    series: Optional[SeriesSimple]

    class Config:
        orm_mode = True
