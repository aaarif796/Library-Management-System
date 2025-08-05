from pydantic import BaseModel, EmailStr, field_validator, model_validator
from datetime import date
import re
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

# Book Model
class Book(BaseModel):
    book_id: str
    library_id: str
    title: str
    isbn: str
    total_copies: int| None
    publication_date: date
    available_copies: int | None


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

    @field_validator("isbn", mode="before")
    def validate_and_clean_isbn(cls, v):
        if not v:
            return None
        clean = re.sub(r"[-\s]", "", v)
        if (len(clean) == 13 or len(clean)==10) and clean.isdigit():
            return clean
        raise ValueError("Invalid ISBN-13 or ISBN-10")

    @field_validator("available_copies")
    def validate_available_copies(cls, v:int | None ) ->int | None:
        """
            Validation available copies which should not be less than 0 or 0
        :param v:
        :return:
        """
        if v is None:
            return None
        return max(v, 0)

    @field_validator("publication_date")
    def validate_publication_date(cls, v: date) -> date:
        """
            Validation publication date which should not be more than present date
        :param v:
        :return:
        """
        if v > date.today():
            logger.exception("It's not possible to give the future date")
            v = date(2010, 10, 10)
        return v



# Library Model
class Library1(BaseModel):
    library_id: int
    Name: str
    campus_location: str
    contact_email: EmailStr
    phone_number: str

    @field_validator('library_id')
    def validate_library_id(cls, v: int) -> int:
        """
        Validating the library id which must be more than 0
        :param v:
        :return:
        """
        if v<1:
            raise ValueError("Primary id should not be 0 or less than it")
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
        pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$"

        if not re.match(pattern, v):
            raise ValueError("Invalid Email Address")
        return str.lower(v)

    @field_validator('phone_number')
    def validate_phone_number(cls, data: str) -> str:
        data = re.sub(r'\D', '', data)  # strips everything except digits
        if not data:
            raise ValueError("Phone number is empty")

        if data.startswith("00"):
            data = data[2:]
        if data.startswith("+"):
            data = data[1:]

        if len(data) > 10:
            country_code = data[:-10]
            national_number = data[-10:]
        else:
            country_code = "91"
            national_number = data.zfill(10)

        return f"+{country_code}-{national_number[:3]}-{national_number[3:6]}-{national_number[6:10]}"

# Author Model
class Author(BaseModel):
    author_id: str
    first_name: str
    last_name: str | None
    birth_date: date | None
    nationality: str | None
    biography: str | None

    @field_validator("first_name", "last_name", mode="before")
    def capitalize_names(cls, v):
        return v.strip().capitalize()


    @field_validator("birth_date")
    def validate_birth_date(cls, v: date | None) -> date| None:
        """
            It's used to validate the date
        :param v:
        :return:
        """
        if not v:
            return None
        if v > date.today():
            raise ValueError("It's invalid birth date")
        return v

    @field_validator("nationality")
    def validate_nationality(cls, v: str | None)-> str| None:
        """
        It's used to validate and reformat the nationality in proper way
        :param v:
        :return:
        """
        if not v:
            return None
        trimmed = v.strip()
        split_name = trimmed.split()
        capitalized = [name.capitalize() for name in split_name]
        nationality = ' '.join(capitalized)
        return nationality



# Borrowing Model
class Borrowing(BaseModel):
    borrowing_id: int
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: date
    late_fee: int

    @field_validator('borrowing_id')
    def validate_borrowing_id(cls, v: int) -> int:
        """
        Validating the primary key
        :param v:
        :return:
        """
        if v<1:
            raise ValueError("Primary key should not be 0 or less than it")
        return v

    @field_validator('book_id')
    def validate_book_id(cls, v: int) -> int:
        """
        Validating the primary key
        :param v:
        :return:
        """
        if v < 1:
            raise ValueError("Primary key should not be 0 or less than it")
        return v

    @field_validator('member_id')
    def validate_member_id(cls, v: int) -> int:
        """
        Validating the primary key
        :param v:
        :return:
        """
        if v < 1:
            raise ValueError("Primary key should not be 0 or less than it")
        return v

    @model_validator(mode = "after")
    def validate_date(self):
        borrow_d = self.borrow_date
        due_d = self.due_date
        if borrow_d > due_d:
            raise ValueError("Data Error borrow date is before than due date")
        return self

    @field_validator('late_fee')
    def validate_late_fee(cls, v: int) -> int:
        if v is None:
            return 0
        return v


# Member Model
class Member(BaseModel):
    member_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    member_type: str
    registration_date: date

    @field_validator('member_id')
    def validate_member_id(cls, v: int) -> int:
        """
        Validating the author id which must be more than 0
        :param v:
        :return:
        """
        if v < 1:
            raise ValueError("Primary id should not be 0 or less than it")
        return v

    @field_validator('last_name')
    def validate_last_name(cls, v: str) -> str:
        """
            It's used to keep the last name in proper format
        :param v:
        :return:
        """
        trimmed = v.strip()
        if len(trimmed.split()) > 1:
            raise ValueError("Surname should be of only word")
        return trimmed.capitalize()

    @field_validator('first_name')
    def validate_first_name(cls, v: str) -> str:
        """
            It's used to keep the first name in proper format
        :param v:
        :return:
        """
        trimmed = v.strip()
        split_name = trimmed.split()
        capitalized = [name.capitalize() for name in split_name]
        first_name = ' '.join(capitalized)
        return first_name

    @field_validator('email')
    def validate_contact_email(cls, v: str) -> str:
        pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid Email Address")
        return str.lower(v)

    @field_validator('phone')
    def validate_phone(cls, data: str) -> str:
        data = re.sub(r'\D', '', data)
        if not data:
            raise ValueError("Phone number is empty")
        if data.startswith("00"):
            data = data[2:]
        if data.startswith("+"):
            data = data[1:]
        if len(data) > 10:
            country_code = data[:-10]
            national_number = data[-10:]
        else:
            country_code = "91"
            national_number = data.zfill(10)
        return f"+{country_code}-{national_number[:3]}-{national_number[3:6]}-{national_number[6:10]}"


    @field_validator('member_type')
    def validate_member_type(cls, v: str) -> str:
        v = v.lower()
        if v not in {"student", "faculty"}:
            raise ValueError("Invalid Member type")
        return v

# Review Model
class Review(BaseModel):
    review_id: int
    book_id: int
    member_id: int
    rating: int
    comment: str
    review_date: date

    @field_validator('review_id')
    def validate_review_id(cls, v: int) -> int:
        """
        Check is there any negative number of 0 is there or not in primary key
        :param v:
        :return:
        """
        if v<= 0:
            raise ValueError("Invalid review id")
        return v

    @field_validator('book_id')
    def validate_book_id(cls, v: int) -> int:
        """
        Check is there any negative number of 0 is there or not in primary key
        :param v:
        :return:
        """
        if v <= 0:
            raise ValueError("Invalid book_id")
        return v

    @field_validator('member_id')
    def validate_member_id(cls, v: int) -> int:
        """
        Check is there any negative number of 0 is there or not in primary key
        :param v:
        :return:
        """
        if v <= 0:
            raise ValueError("Invalid member_id")
        return v

    @field_validator('rating')
    def validate_rating(cls, rating: int) -> int:
        if rating < 1 or rating > 5:
            raise ValueError("Rating should be between 1-5")
        return rating



# Category Model
class Category(BaseModel):
    category_id: int
    name: str
    description: str

    @field_validator('category_id')
    def validate_category_id(cls, v):
        """
        Check is there any negative number of 0 is there or not in primary key
        :param v:
        :return:
        """
        if v <= 0:
            raise ValueError("Invalid member_id")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        """
        It's used to validate the name in first capital letter and proper spacing
        :param v:
        :return:
        """
        trimmed = v.strip()
        split_name = trimmed.split()
        capitalized = [name.capitalize() for name in split_name]
        name = ' '.join(capitalized)
        return name


