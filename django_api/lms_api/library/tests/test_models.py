import pytest
from .factories import LibraryFactory, AuthorFactory, CategoryFactory, BookFactory, MemberFactory, BorrowingFactory, ReviewFactory

@pytest.mark.django_db
def test_library_str():
    library = LibraryFactory(l_name="Central Library")
    assert str(library) == "Central Library"

@pytest.mark.django_db
def test_author_str():
    author = AuthorFactory(first_name="John")
    assert str(author) == "John"

@pytest.mark.django_db
def test_category_str():
    category = CategoryFactory(name="Programming")
    assert str(category) == "Programming"

@pytest.mark.django_db
def test_book_str():
    book = BookFactory(title="Clean Code")
    assert str(book) == "Clean Code"

@pytest.mark.django_db
def test_member_str():
    member = MemberFactory(first_name="Alice")
    assert str(member) == "Alice"

@pytest.mark.django_db
def test_borrowing_str():
    borrowing = BorrowingFactory(member__first_name="Bob")
    assert str(borrowing) == "Bob"

@pytest.mark.django_db
def test_review_str():
    review = ReviewFactory(member__first_name="Eve")
    assert str(review) == "Eve"