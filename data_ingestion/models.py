import datetime
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base, foreign

engine = db.create_engine("mysql+pymysql://root:root@127.0.0.1:3306/LMS_ORM")
Base = declarative_base()
# meta = db.MetaData()

class Library(Base):
    __table_name__ = "Library"
    library_id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    name = db.Column(db.String)
    campus_location = db.Column(db.String)
    email = db.Column(db.String)

class Book(Base):
    __table_name__ = "Book"
    book_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    library_id = db.Column(db.Integer, db.ForeignKey('Library.library_id'))
    title = db.Column(db.String)
    isbn = db.Column(db.String)
    publication_date = db.Column(db.Date)
    total_copies = db.Column(db.Integer)
    available_copies = db.Column(db.Integer)

class Author(Base):
    __table_name__ = "Author"
    author_id = db.Column(db.Integer, priamry_key = True, autoincrement = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String)
    biography = db.Column(db.Text)

class BookAuthor(Base):
    __table_name__ = "BookAuthor"

class Category(Base):
    __table_name = "Category"
    category_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    description = db.Column(db.Text)

class BookCategory(Base):
    __table_name__ = "BookCategory"


class Borrowing(Base):
    __table_name__ = "Borrowing"
    borrowing_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'))
    member_id = db.Column(db.Integer, db.ForeignKey('Member.member_id'))
    borrow_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    late_fee = db.Column(db.Integer)

class Member(Base):
    __table_name__ = "Member"
    member_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    member_type = db.Column(db.String)
    registration_date = db.Column(db.Date)

class Review(Base):
    __table_name__ = "Review"
    review_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'))
    member_id = db.Column(db.Integer, db.ForeignKey('Member.member_id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    review_date = db.Column(db.Date)



