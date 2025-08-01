import json
import sys
import logging
from schemas import Book
from typing import List, Dict, Any

file_path: str = sys.argv[1]
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


with open(file_path, 'r') as f:
    books_raw: List[Dict[str, Any]] = json.load(f)
    logging.info("File open successfully")

valid_books: List[Dict[str, Any]] = []
invalid_books: List[Dict[str, Any]] = []

for book in books_raw:
    try:
        validated: Book = Book(**book)
        valid_books.append(validated.model_dump(mode = "json"))
    except Exception as e:
        invalid_books.append({
            "record": book,
            "error": str(e)
        })
        logging.warning(f"Record is not in specific format. Record no.{book}")

valid_path: str = "validated_books.json"
invalid_path: str = "invalid_books.json"

with open(valid_path,"w") as f:
    json.dump(valid_books, f, indent = 4)
    logging.info("This is an info message")

with open(invalid_path, "w") as f:
    json.dump(invalid_books, f, indent = 4)

# To run it we have to use
# python data_ingestion\books_processor.py data_ingestion\book_records.json