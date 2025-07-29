import json
from data_validation import Book
from typing import List, Dict, Any

file_path: str = "sample_data_of_book.json"

with open(file_path, 'r') as f:
    books_raw: List[Dict[str, Any]] = json.load(f)

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

valid_path: str = "validated_books.json"
invalid_path: str = "invalid_books.json"

with open(valid_path,"w") as f:
    json.dump(valid_books, f, indent = 4)

with open(invalid_path, "w") as f:
    json.dump(invalid_books, f, indent = 4)

