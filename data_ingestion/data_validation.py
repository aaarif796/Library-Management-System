from pydantic import BaseModel, EmailStr, Field, field_validator,ValidationError, ValidationInfo
import json
from typing import List, Dict, Any
from datetime import date
import re
import json

# "book_id": 2,
# "title": "Remember dream position",
# "author": "Melissa White",
# "isbn": "978-0-631-04059-0",
# "available_copies": 0,
# "total_copies": 5,
# "publication": "2002-02-03"
class Book(BaseModel):
    book_id: int
    title: str
    author: str
    isbn: str
    available_copies: int
    total_copies: int
    publication: date

    @field_validator("isbn")
    def validate_isbn(cls, v:str) ->str:
        cleaned = re.sub(r"[-\s]", "",v)
        if len(cleaned) not in (10,13):
            raise ValueError("ISBN must be 10 or 13 digits")
        if not cleaned.isdigit():
            raise ValueError("ISBN must contain number")
        return cleaned

    @field_validator("available_copies")
    def validate_available_copies(cls, v:int) ->int:
        if v <= 0:
            raise ValidationError("Available copies won't be less than 0")
        return v

