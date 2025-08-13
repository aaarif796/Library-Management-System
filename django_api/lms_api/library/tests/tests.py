from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from library.models import Library_Col, Book

class LibraryTestCase(TestCase):
    def setUp(self):
        # Create a library first, because Book has a FK to Library_Col
        self.library = Library_Col.objects.create(
            l_name="Central Library",
            campus_location="Main Campus",
            contact_email="central@library.com",
            phone_number="1234567890"
        )
    def test_library_creation(self):
        """Test that the library was created successfully"""
        library = Library_Col.objects.get(l_name="Central Library")
        self.assertEqual(library.l_name, "Central Library")
        self.assertEqual(library.campus_location, "Main Campus")
        self.assertEqual(library.contact_email, "central@library.com")
        self.assertEqual(library.phone_number, "1234567890")

    def test_library_str_method(self):
        """Test Library_Col __str__ method"""
        self.assertEqual(str(self.library), "Central Library")



# Book Test Case
class BookTestCase(TestCase):
    def setUp(self):
        # Create a library first (Book has FK to Library_Col)
        self.library = Library_Col.objects.create(
            l_name="Central Library",
            campus_location="Main Campus",
            contact_email="central@library.com",
            phone_number="1234567890"
        )

        # Create a book linked to that library
        self.book = Book.objects.create(
            library=self.library,
            title="Albatross",
            isbn="4342467631",
            publication_date=datetime(2010, 10, 21),
            total_copies=10,
            available_copies=8
        )

    def test_book_creation(self):
        """Test that the book was created successfully"""
        book = Book.objects.get(title="Albatross")
        self.assertEqual(book.title, "Albatross")
        self.assertEqual(book.isbn, "4342467631")
        self.assertEqual(book.total_copies, 10)
        self.assertEqual(book.available_copies, 8)
        self.assertEqual(book.library.l_name, "Central Library")

    def test_book_str_method(self):
        """Test Book __str__ method"""
        self.assertEqual(str(self.book), "Albatross")


