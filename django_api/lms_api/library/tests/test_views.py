from django.test import TestCase
from rest_framework.test import APIClient
from library.tests.factories import BookFactory, MemberFactory, BorrowingFactory, CategoryFactory

class BookViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list(self):
        BookFactory.create_batch(3)
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 3)

    def test_borrow_book(self):
        book = BookFactory(available_copies=3)
        member = MemberFactory()
        response = self.client.post(f"/api/books/{book.id}/borrow-book/", {
            "member_id": member.id
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Book borrowed successfully")

    def test_return_book(self):
        borrowing = BorrowingFactory()
        response = self.client.post(f"/api/books/{borrowing.book.id}/return-book/", {
            "member_id": borrowing.member.id
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("late_fee", response.json())

    def test_category_filter(self):
        category = CategoryFactory(name="Programming")
        book = BookFactory()
        book.categories.add(category)
        response = self.client.get("/api/books/category/?name=Programming")
        self.assertEqual(response.status_code, 200)

    def test_availability(self):
        book = BookFactory(available_copies=1)
        response = self.client.get(f"/api/books/{book.id}/availability/")
        self.assertEqual(response.status_code, 200)

    def test_search_books(self):
        book = BookFactory(title="Clean Code")
        response = self.client.get("/api/books/search/?search=clean")
        self.assertEqual(response.status_code, 200)

class MemberViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_member_borrowings(self):
        borrowing = BorrowingFactory()
        response = self.client.get(f"/api/members/{borrowing.member.id}/borrowings/")
        self.assertEqual(response.status_code, 200)

class StatisticsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_statistics_endpoint(self):
        response = self.client.get("/api/statistics/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_books", response.json())