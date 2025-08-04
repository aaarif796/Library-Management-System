import argparse
import logging
import os
from datetime import date, datetime

from api_client import OpenLibraryClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Author, Book
from schemas import BookSchema, AuthorSchema


def configure_logging(level="INFO", log_path="etl.log"):
    numeric = getattr(logging, level.upper(), logging.INFO)
    fmt = "%(asctime)s [%(levelname)s] %(message)s"
    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # File handler
    fh = logging.FileHandler(log_path)
    fh.setLevel(numeric)
    fh.setFormatter(logging.Formatter(fmt))

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(numeric)
    ch.setFormatter(logging.Formatter(fmt))

    logging.basicConfig(level=numeric, handlers=[fh, ch])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True, help="Author name to search for")
    parser.add_argument("--limit", type=int, default=10, help="Number of books to fetch")
    parser.add_argument("--db", "--database-url", required=True,
                        help="SQLAlchemy DB URL, e.g. mysql+pymysql://user:pass@host/db")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def get_session(db_url: str):
    engine = create_engine(db_url, echo=False, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def extract_author_info(author_doc):
    key = str(author_doc.get("key", "")).split("/")[-1]
    name = author_doc.get("name", "Unknown").strip().title()
    parts = name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""
    subjects = author_doc.get("top_subjects", [])
    subjects_str = ", ".join(subjects) if isinstance(subjects, list) else ""

    return AuthorSchema(
        author_id=key,
        first_name=first_name,
        last_name=last_name,
        subjects=subjects_str,
    )


def extract_book_info(work_detail, client, author_id: str):
    book_id = work_detail.get("key", "").split("/")[-1]
    title = work_detail.get("title", "Untitled").title()

    # Get edition metadata
    edition_key = work_detail.get("key", "").split("/")[-1]
    edition_url = f"/works/{edition_key}/editions.json"
    edition_data = client.get(edition_url)

    if not edition_data:
        logging.warning(f"Failed to get edition data for {edition_key}")
        return None

    editions = edition_data.get("entries", [])
    if not editions:
        return None

    edition = editions[0]

    # Parse publication date
    raw_date = edition.get("publish_date", "")
    publication_date = None
    for fmt in ("%B %d, %Y", "%Y-%m-%d", "%Y", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            publication_date = datetime.strptime(raw_date, fmt).date()
            break
        except Exception:
            continue

    if not publication_date:
        logging.warning(f"Unrecognized date format '{raw_date}' for book '{title}'")
        publication_date = date(2024, 1, 1)  # fallback default

    # Normalize ISBN
    isbn = None
    for key in ("isbn_13", "isbn_10"):
        if key in edition:
            isbn = BookSchema.validate_and_clean_isbn(edition[key][0])
            break

    language = (edition.get("languages", [{}])[0].get("key", "").split("/")[-1]
                if edition.get("languages") else "eng")

    return Book(
        book_id=book_id,
        author_id=author_id,  # ← Use the consistent author_id
        title=title,
        publication_date=publication_date,
        isbn=isbn,
        language=language
    )


def main():
    args = parse_args()
    configure_logging(args.log_level)
    client = OpenLibraryClient()
    session = get_session(args.db)

    search_result = client.search_author(args.author)
    if not search_result["docs"]:
        logging.error("Author not found.")
        return

    author_doc = search_result["docs"][0]
    author_schema = extract_author_info(author_doc)
    author_key = str(author_doc.get("key", "")).split("/")[-1]

    author = session.get(Author, author_schema.author_id)
    if not author:
        author = Author(**author_schema.model_dump())
        session.add(author)
        session.commit()
        logging.info(f"Inserted author: {author.first_name} {author.last_name}")
    else:
        logging.info(f"Author already exists: {author.first_name} {author.last_name}")

    works = client.get_author_works(author_key, args.limit).get("entries", [])

    for work in works:
        work_key = work.get("key")
        try:
            work_detail = client.get_work_detail(work_key)
            book_id = work_detail.get("key", "").split("/")[-1]

            if session.get(Book, book_id):
                logging.info(f"Book already exists: {book_id}")
                continue

            book = extract_book_info(work_detail, client, author.author_id)
            if book is None:
                logging.warning(f"Skipping book with invalid data: {work.get('title', 'Unknown')}")
                continue

            session.add(book)
            session.commit()
            logging.info(f"Inserted book: {book.title}")

        except Exception as e:
            session.rollback()
            logging.error(f"Failed to insert book: {work.get('title', 'Unknown')} | Error: {e}")

    session.close()


if __name__ == "__main__":
    main()
