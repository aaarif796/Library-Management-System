import argparse
import json
from api_client import OpenLibraryClient

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True, help="Author name to search for")
    parser.add_argument("--limit", type=int, default=10, help="Number of books to fetch")
    parser.add_argument("--output", help="Output JSON file to save data")
    return parser.parse_args()

def main():
    args = parse_args()
    client = OpenLibraryClient()
    collected_data = []

    print(f"Searching for author: {args.author}")
    search_result = client.search_author(args.author)

    if not search_result["docs"]:
        print("Author not found.")
        return

    author_key = search_result["docs"][0]["key"]
    print(f"Author found: {author_key}")

    works = client.get_author_works(author_key, args.limit)
    print(f"Found {len(works.get('entries', []))} works. Fetching details...")

    for work in works.get("entries", []):
        work_key_path = work.get("key")
        try:
            detail = client.get_work_detail(work_key_path)
            collected_data.append(detail)
            print(f"Collected: {detail.get('title', 'No Title')}")
        except Exception as e:
            print(f"Skipped: {work.get('title', 'Unknown')} | Error: {e}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(collected_data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(collected_data)} records to '{args.output}'")
    else:
        print(json.dumps(collected_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
