from xml.dom import VALIDATION_ERR

from pydantic import BaseModel, EmailStr, Field, validator,ValidationError
import json
from datetime import date


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
#
# class Book(BaseModel):
#     name: str
#     age: int
#     grade: str
#
#     @validator('name'):
#     def name_must_not_be_empty(cls,v):
#         if not v.strip():
#             raise ValueError("Name cannot be empty")
#         return v
#
#     @validator('age')
#     def age_must_be_positive(cls, v):
#         if v<0:
#             raise ValueError('Age must be positive')
#         return v
#

with open('sample_data_of_book.json', 'r') as f:
    data = json.load(f)

for record in data:
    try:
        book = Book(**record)
        print(f"Valid employee record:{book.title}")
    except ValidationError as e:
        print(f"Invalid employee record:{record['title']}")
        print(f'Errors:{e.errors()}')
