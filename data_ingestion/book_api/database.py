from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()

class BookModel(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, nullable=True)
    publish_year = Column(Integer, nullable=True)
    pages = Column(Integer, nullable=True)
    language = Column(String, default="en")

engine = create_engine("postgresql+psycopg2://user:pass@localhost/booksdb")
SessionLocal = sessionmaker(bind=engine)

def get_session() -> Session:
    return SessionLocal()

def init_db():
    Base.metadata.create_all(bind=engine)