import requests
import time

class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org"

    def __init__(self, rate_limit: float = 1.0):
        self.last_request_time = 0
        self.rate_limit = rate_limit

    def get(self, endpoint):
        url = self.BASE_URL + endpoint
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def _wait_if_necessary(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def search_author(self, author_name):
        self._wait_if_necessary()
        response = requests.get(f"{self.BASE_URL}/search/authors.json", params={"q": author_name})
        response.raise_for_status()
        return response.json()

    def get_author_works(self, author_key, limit):
        self._wait_if_necessary()
        response = requests.get(f"{self.BASE_URL}/authors/{author_key}/works.json", params={"limit": limit})
        response.raise_for_status()
        return response.json()

    def get_book_details(self, olid_or_isbn: str, is_isbn: bool = False):
        self._wait_if_necessary()
        if is_isbn:
            url = f"{self.BASE_URL}/isbn/{olid_or_isbn}.json"
        else:
            url = f"{self.BASE_URL}/books/{olid_or_isbn}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_work_detail(self, work_key_path):
        self._wait_if_necessary()
        url = f"{self.BASE_URL}{work_key_path}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
