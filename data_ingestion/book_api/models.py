import pymysql
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

connection = pymysql.connect(host='127.0.0.1', user='root', password='root')
cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS OpenBook")
connection.close()

engine = db.create_engine("mysql+pymysql://root:root@127.0.0.1:3306/OpenBook")
Base = declarative_base()


class Author(Base):
    __tablename__ = "Author"
    author_id = db.Column(db.String(15), primary_key= True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    subjects = db.Column(db.Text)
    b_author = relationship("Book", back_populates="a_book")


class Book(Base):
    __tablename__ = "Book"
    book_id = db.Column(db.String(15), primary_key= True)
    author_id = db.Column(db.String(15), db.ForeignKey("Author.author_id"))
    title = db.Column(db.String(100))
    publication_date = db.Column(db.Date)
    description = db.Column(db.Text)
    total_copies = db.Column(db.Integer)
    available_copies = db.Column(db.Integer)
    a_book = relationship("Author", back_populates="b_author")

if __name__ == "__main__":
    Base.metadata.create_all(engine)