from pydantic import BaseModel

class TagBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class TagCreate(BaseModel):
    name: str
