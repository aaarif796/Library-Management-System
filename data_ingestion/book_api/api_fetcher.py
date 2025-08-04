import argparse
import json
from uuid import uuid4
from datetime import date
from api_client import OpenLibraryClient


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True, help="Author name to search for")
    parser.add_argument("--limit", type=int, default=10, help="Number of books to fetch")
    parser.add_argument("--output", help="Output JSON file to save structured data")
    return parser.parse_args()


def extract_author_info(author_obj):
    """Extract author_id, first_name, last_name"""
    key = author_obj.get("key", "").split("/")[-1]
    name = author_obj.get("name", "Unknown").strip()
    parts = name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""
    return {
        "author_id": key,
        "first_name": first_name,
        "last_name": last_name,
        "subjects": None  # Optional: Fill this if needed
    }


def extract_book_info(work_detail, author_id):
    """Extract book information"""
    return {
        "book_id": work_detail.get("key", "").split("/")[-1],
        "author_id": author_id,
        "title": work_detail.get("title", "Untitled"),
        "description": (
            work_detail.get("description", {}).get("value", "")
            if isinstance(work_detail.get("description"), dict)
            else work_detail.get("description", "")
        ),
        "publication_date": "2024-01-01",  # Placeholder; OpenLibrary often lacks this
        "total_copies": 10,
        "available_copies": 10,
    }


def main():
    args = parse_args()
    client = OpenLibraryClient()
    structured_data = []

    print(f"Searching for author: {args.author}")
    search_result = client.search_author(args.author)

    if not search_result["docs"]:
        print("Author not found.")
        return

    author_doc = search_result["docs"][0]
    author_key = author_doc["key"]
    print(f"Author found: {author_key}")

    works = client.get_author_works(author_key, args.limit)
    work_entries = works.get("entries", [])
    print(f"Found {len(work_entries)} works. Fetching details...")

    for work in work_entries:
        work_key_path = work.get("key")
        try:
            detail = client.get_work_detail(work_key_path)
            # Get first author details (you can extend to multiple later)
            author_info = extract_author_info(author_doc)
            book_info = extract_book_info(detail, author_info["author_id"])
            structured_data.append({
                "author": author_info,
                "book": book_info
            })
            print(f"Collected: {book_info['title']}")
        except Exception as e:
            print(f"Skipped: {work.get('title', 'Unknown')} | Error: {e}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(structured_data)} structured records to '{args.output}'")
    else:
        print(json.dumps(structured_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
