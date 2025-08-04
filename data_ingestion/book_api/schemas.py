from pydantic import BaseModel, field_validator, constr
from typing import Optional
from datetime import date, datetime
import re


class AuthorSchema(BaseModel):
    author_id: str
    first_name: str
    last_name: str
    subjects: str

    @field_validator("first_name", "last_name", mode="before")
    def capitalize_names(cls, v):
        return v.strip().capitalize()


class BookSchema(BaseModel):
    book_id: str
    author_id: str
    title: str
    publication_date: date
    isbn: Optional[str]
    language: Optional[str]

    @field_validator("title", mode="before")
    def normalize_title(cls, v):
        return v.title().strip()

    @field_validator("isbn", mode="before")
    def validate_and_clean_isbn(cls, v):
        if not v:
            return None
        clean = re.sub(r"[-\s]", "", v)
        if len(clean) == 13 and clean.isdigit():
            return clean
        raise ValueError("Invalid ISBN-13")

    @field_validator("publication_date", mode= "before")
    def validate_pub_date(cls, v):
        if isinstance(v, date):
            return v

        if isinstance(v, str):
            for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%Y", "%Y-%m-%dT%H:%M:%S.%f"):
                try:
                    return datetime.strptime(v.strip(), fmt).date()
                except ValueError:
                    continue

        if not v or not isinstance(v, date):
            return date(2024, 1, 1)
        return v