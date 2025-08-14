from django.test import TestCase
from ..serializers import BookSerializer, MemberSerializer
from .factories import BookFactory, MemberFactory

class BookSerializerTests(TestCase):
    def test_book_serializer_fields(self):
        book = BookFactory()
        data = BookSerializer(book).data
        self.assertIn("title", data)
        self.assertEqual(data["isbn"], book.isbn)

class MemberSerializerTests(TestCase):
    def test_member_serializer_email_lowercase(self):
        member = MemberFactory(email="TEST@EMAIL.COM")
        serializer = MemberSerializer(member)
        self.assertEqual(serializer.data["email"], member.email.lower())
