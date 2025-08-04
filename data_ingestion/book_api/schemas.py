from typing import Optional, List
from pydantic import BaseModel, Field, validator

class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    publish_year: Optional[int] = None
    pages: Optional[int] = None
    language: Optional[str] = "en"

    @validator("isbn")
    def normalise_isbn(cls, v):
        return v.replace("-", "").replace(" ", "") if v else None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True