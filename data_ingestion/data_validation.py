from pydantic import BaseModel, EmailStr, Field, field_validator,ValidationError, ValidationInfo
import json
from typing import List, Dict, Any
from datetime import date
import re
import json


class Book(BaseModel):
    book_id: int
    library_id: int
    title: str
    isbn: str
    total_copies: int
    publication_date: date
    available_copies: int

    @field_validator('book_id')
    def validate_book_id(cls, v: int) -> int:
        """
            This function is used to validate the book_id which should not be negative
        :param v:
        :return:
        """
        if v<1:
            raise ValidationError("Book id cannot be negative")
        return v

    @field_validator('library_id')
    def validate_library_id(cls, v: int) -> int:
        """
            This function is used to validate the library_id which check it should not be positive
        :param v:
        :return:
        """
        if v<1:
            raise "Library_id should be positive"
        return v

    @field_validator('title')
    def validate_title(cls, v:str) ->str:
        """
            In this function first trim the string,
            split the string with the space
            and add capitalization function before joining
            after that join with the space
        :param v:
        :return:
        """
        trimmed = v.strip()
        split_title = trimmed.split()
        capitalized = [title.capitalize() for title in split_title]
        concat_title = ' '.join(capitalized)
        return concat_title

    @field_validator("isbn")
    def validate_isbn(cls, v:str) ->str:
        """
            Validationg the isbn where isbn will contain either 10 or 13 digits
        :param v:
        :return:
        """
        cleaned = re.sub(r"[-\s]", "",v)
        if len(cleaned) not in (10,13):
            raise ValueError("ISBN must be 10 or 13 digits")
        if not cleaned.isdigit():
            raise ValueError("ISBN must contain number")
        return cleaned

    @field_validator("available_copies")
    def validate_available_copies(cls, v:int) ->int:
        """
            Validation available copies which should not be less than 0 or 0
        :param v:
        :return:
        """
        if v <= 0:
            raise ValidationError("Available copies won't be less than 0")
        return v

    @field_validator("publication_date")
    def validate_publication_date(cls, v: date) -> date:
        """
            Validation publication date which should not be more than present date
        :param v:
        :return:
        """
        if v > date.today():
            raise ValidationError("It's not possible to give the future date")
        return v

class Library(BaseModel):
    library_id: int
    Name: str
    campus_location: str
    contact_email: str
    phone_number = int

    @field_validator('library_id')
    def validate_library_id(cls, v: int) -> int:
        """
        Validating the library id which must be more than 0
        :param v:
        :return:
        """
        if v<1:
            raise ValidationError("Primary id should not be 0 or less than it")
        return v

    @field_validator('Name')
    def validate_name(cls, v:str) ->str:
        """
            In this function first trim the string,
            split the string with the space
            and add capitalization function before joining
            after that join with the space
        :param v:
        :return:
        """
        trimmed = v.strip()
        split_name = trimmed.split()
        capitalized = [name.capitalize() for name in split_name]
        library_name = ' '.join(capitalized)
        return library_name

    @field_validator('contact_email')
    def validate_contact_email(cls, v: str) -> str:
        """
        Validating the email which must follow email pattern and it's should be in lowercase
        :param v:
        :return:
        """
        pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValidationError("Invalid Email Address")
        return str.lower(v)

    @field_validator('phone_number')
    def validate_phone_number(cls, v:str) -> str:
        """
            Validating the phone number
        :param v:
        :return:
        """
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
        return str.lower(v)

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




