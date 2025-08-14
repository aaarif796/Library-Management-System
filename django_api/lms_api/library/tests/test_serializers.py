import pytest
from ..serializers import BookSerializer, MemberSerializer
from .factories import BookFactory, MemberFactory

@pytest.mark.django_db
def test_book_serializer_fields():
    book = BookFactory()
    data = BookSerializer(book).data
    assert "title" in data
    assert data["isbn"] == book.isbn

@pytest.mark.django_db
def test_member_serializer_email_lowercase():
    member = MemberFactory(email="TEST@EMAIL.COM")
    serializer = MemberSerializer(member)
    assert serializer.data["email"] == member.email.lower()
""",

    # tests/test_views.py
    "lms/tests/test_views.py": """\
import pytest
from lms.tests.factories import BookFactory, MemberFactory, BorrowingFactory, CategoryFactory
from django.utils import timezone

@pytest.mark.django_db
def test_book_list(api_client):
    BookFactory.create_batch(3)
    response = api_client.get("/api/books/")
    assert response.status_code == 200
    assert len(response.json()) >= 3

@pytest.mark.django_db
def test_borrow_book(api_client):
    book = BookFactory(available_copies=3)
    member = MemberFactory()
    response = api_client.post(f"/api/books/{book.id}/borrow-book/", {
        "member_id": member.id
    }, format="json")
    assert response.status_code == 201
    assert response.json()["message"] == "Book borrowed successfully"

@pytest.mark.django_db
def test_return_book(api_client):
    borrowing = BorrowingFactory()
    response = api_client.post(f"/api/books/{borrowing.book.id}/return-book/", {
        "member_id": borrowing.member.id
    }, format="json")
    assert response.status_code == 200
    assert "late_fee" in response.json()

@pytest.mark.django_db
def test_category_filter(api_client):
    category = CategoryFactory(name="Programming")
    book = BookFactory()
    book.categories.add(category)
    response = api_client.get("/api/books/category/?name=Programming")
    assert response.status_code == 200

@pytest.mark.django_db
def test_availability(api_client):
    book = BookFactory(available_copies=1)
    response = api_client.get(f"/api/books/{book.id}/availability/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_search_books(api_client):
    book = BookFactory(title="Clean Code")
    response = api_client.get("/api/books/search/?search=clean")
    assert response.status_code == 200

@pytest.mark.django_db
def test_member_borrowings(api_client):
    borrowing = BorrowingFactory()
    response = api_client.get(f"/api/members/{borrowing.member.id}/borrowings/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_statistics_endpoint(api_client):
    response = api_client.get("/api/statistics/")
    assert response.status_code == 200
    assert "total_books" in response.json()