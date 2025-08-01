import pymysql
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship

connection = pymysql.connect(host='127.0.0.1', user='root', password='root')
cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS LMS_ORM")
connection.close()

engine = db.create_engine("mysql+pymysql://root:root@127.0.0.1:3306/LMS_ORM")
Base = declarative_base()

class Library1(Base):
    __tablename__ = "Library1"
    library_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50))
    campus_location = db.Column(db.String(80))
    contact_email = db.Column(db.String(40))
    phone_number = db.Column(db.String(25))
    books = relationship("Book", back_populates="library1")
    __table_args__ = (
        db.UniqueConstraint('contact_email', name='contact_email_unique'),
        db.UniqueConstraint('phone_number', name='phone_number_unique'),
    )


class Book(Base):
    __tablename__ = "Book"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    library_id = db.Column(db.Integer, db.ForeignKey('Library1.library_id'))
    title = db.Column(db.String(50))
    isbn = db.Column(db.String(13))
    publication_date = db.Column(db.Date)
    total_copies = db.Column(db.Integer)
    available_copies = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('isbn', name='uq_book_isbn'),)
    library1 = relationship("Library1", back_populates="books")  # fixed
    borrowing_b = relationship("Borrowing", back_populates="book_b")  # fixed
    r_book = relationship("Review", back_populates="b_review")  # fixed
    ba_book = relationship("BookAuthor", back_populates="b_BookAuthor")  # fixed
    bc_book = relationship("BookCategory", back_populates="b_BookCategory")  # added



class Author(Base):
    __tablename__ = "Author"
    author_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String(30))
    biography = db.Column(db.Text)
    ba_Author = relationship("BookAuthor",back_populates="a_BookAuthor")



class BookAuthor(Base):
    __tablename__ = "BookAuthor"
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'), primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('Author.author_id') ,primary_key = True)
    b_BookAuthor = relationship("Book",back_populates="ba_book")
    a_BookAuthor = relationship("Author", back_populates="ba_Author")

    __table_args__ = (db.UniqueConstraint('book_id','author_id', name='uq_book_isbn'),)


class Category(Base):
    __tablename__ = "Category"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    bc_Category = relationship("BookCategory", back_populates="c_BookCategory")


class BookCategory(Base):
    __tablename__ = "BookCategory"
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.category_id'), primary_key=True)
    __table_args__ = (db.UniqueConstraint('book_id','category_id', name='uq_book_isbn'),)
    b_BookCategory = relationship("Book", back_populates="bc_book")
    c_BookCategory = relationship("Category", back_populates="bc_Category")



class Borrowing(Base):
    __tablename__ = "Borrowing"
    borrowing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'))
    member_id = db.Column(db.Integer, db.ForeignKey('Member.member_id'))
    borrow_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    late_fee = db.Column(db.Integer)

    book_b = relationship("Book", back_populates='borrowing_b')
    b_member = relationship("Member", back_populates="m_borrowing")



class Member(Base):
    __tablename__ = "Member"
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(10))
    email = db.Column(db.String(30))
    phone = db.Column(db.String(25))
    member_type = db.Column(db.String(10))
    registration_date = db.Column(db.Date)

    m_borrowing = relationship("Borrowing", back_populates="b_member")  # fixed
    r_member = relationship("Review", back_populates="m_review")  # keep



class Review(Base):
    __tablename__ = "Review"
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'))
    member_id = db.Column(db.Integer, db.ForeignKey('Member.member_id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    review_date = db.Column(db.Date)

    m_review = relationship("Member", back_populates="r_member")
    b_review = relationship("Book", back_populates="r_book")

# Creating tables
Base.metadata.create_all(engine)