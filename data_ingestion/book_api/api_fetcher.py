import argparse
from datetime import date
from api_client import OpenLibraryClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Author, Book


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True, help="Author name to search for")
    parser.add_argument("--limit", type=int, default=10, help="Number of books to fetch")
    parser.add_argument("--db", "--database-url", required=True, help="SQLAlchemy DB url, e.g. mysql+pymysql://user:pass@host/db")
    return parser.parse_args()


def get_session(db_url: str):
    engine = create_engine(db_url, echo=False, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def extract_author_info(author_doc):
    key = author_doc.get("key", "").split("/")[-1]
    name = author_doc.get("name", "Unknown").strip()
    parts = name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""
    return key, first_name, last_name


def extract_book_info(work, author_id):
    book_id = work.get("key", "").split("/")[-1]
    title = work.get("title", "Untitled")
    desc = work.get("description", "")
    if isinstance(desc, dict):
        desc = desc.get("value", "")
    return Book(
        book_id=book_id,
        author_id=author_id,
        title=title,
        description=desc,
        publication_date=date(2024, 1, 1),  # Placeholder
        total_copies=10,
        available_copies=10
    )


def main():
    args = parse_args()
    client = OpenLibraryClient()
    session = get_session(args.db)

    print(f"Searching for author: {args.author}")
    search_result = client.search_author(args.author)
    if not search_result["docs"]:
        print("Author not found.")
        return

    author_doc = search_result["docs"][0]
    author_key, first_name, last_name = extract_author_info(author_doc)

    # Check if author already exists
    author = session.get(Author, author_key)
    if not author:
        author = Author(
            author_id=author_key,
            first_name=first_name,
            last_name=last_name,
            subjects=None
        )
        session.add(author)
        session.commit()
        print(f"Inserted author: {first_name} {last_name}")
    else:
        print(f"Author already exists: {first_name} {last_name}")

    print("Fetching works...")
    works = client.get_author_works(author_key, args.limit).get("entries", [])
    for work in works:
        try:
            detail = client.get_work_detail(work.get("key"))
            book_id = detail.get("key", "").split("/")[-1]

            if session.get(Book, book_id):
                print(f"Book already exists: {book_id}")
                continue

            book = extract_book_info(detail, author_key)
            session.add(book)
            session.commit()
            print(f"Inserted book: {book.title}")
        except Exception as e:
            print(f"Failed to insert book: {work.get('title', 'Unknown')} | Error: {e}")


if __name__ == "__main__":
    main()
