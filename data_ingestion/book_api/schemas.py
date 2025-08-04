from typing import Optional, List
from pydantic import BaseModel, field_validator
from datetime import date


class Author(BaseModel):
    author_id: str
    first_name: str
    last_name: str
    subjects: Optional[List[str]]


class Book(BaseModel):
    book_id: str
    author_id: str
    title: str
    publication_date: date
    description: str
    total_copies: int
    available_copies: int
