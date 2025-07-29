from pydantic import BaseModel, EmailStr, Field, field_validator,ValidationError, ValidationInfo
import json
from typing import List, Dict, Any
from datetime import date
import re
import json


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

class Library(BaseModel):
    library_id: int
    Name: str
    campus_location: str
    contact_email: str
    phone_number = int

    @field_validator('contact_email')
    def validate_contact_email(cls, v: str) -> str:
        pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValidationError("Invalid Email Address")
        return v

    @field_validator('phone_number')
    def validate_phone_number(cls, v:str) -> str:
        pattern = "^[+0-9]+[-\s]*[0-9]+$"
        if not re.match(pattern, v) or len(v)<10:
            raise ValidationError("Invalid Phone number")
        return v


class Author(BaseModel):
    author_id: int
    first_name: str
    last_name: str
    birth_date: date
    nationality: str
    biography: str


class Borrowing(BaseModel):
    borrowing_id: int
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: date
    late_fee: date

class Member(BaseModel):
    member_id: int
    first_name: str
    last_name: str
    email: str
    phone: int
    member_type: str
    registration_date: date

    @field_validator('email')
    def validate_contact_email(cls, v: str) -> str:
        pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValidationError("Invalid Email Address")
        return v

    @field_validator('phone')
    def validate_phone_number(cls, v: str) -> str:
        pattern = "^[+0-9]+[-\s]*[0-9]+$"
        if not re.match(pattern, v) or len(v) < 10:
            raise ValidationError("Invalid Phone number")
        return v

    @field_validator('member_type')
    def validate_member_type(cls, v: str) -> str:
        if v.lower() != "student" or v.lower() != "faculty":
            raise ValidationError("Invalid Member type")
        return v

class Review(BaseModel):
    review_id: int
    book_id: int
    member_id: int
    rating: int
    comment: str
    review_date: date

    @field_validator('rating')
    def validate_rating(cls, rating: int) -> int:
        if rating < 1 or rating > 5:
            raise ValidationError("Rating should be between 1-5")
        return rating

class Category(BaseModel):
    category_id: int
    name: str
    description: str




