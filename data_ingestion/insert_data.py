from datetime import date
from sqlalchemy.orm import Session
from models import engine, Library, Book, Author, BookAuthor, Category, BookCategory, Member, Borrowing, Review

session = Session(bind=engine)

# Libraries
libraries = [
    Library(name="Central Library", campus_location="Main Campus", email="central@university.edu"),
    Library(name="Science Library", campus_location="Science Block", email="science@university.edu"),
    Library(name="Arts Library", campus_location="Arts Wing", email="arts@university.edu"),
]
session.add_all(libraries)
session.commit()

# Authors
authors = [
    Author(first_name="John", last_name="Doe", birth_date=date(1970, 1, 1), nationality="American", biography="Writes fiction."),
    Author(first_name="Jane", last_name="Smith", birth_date=date(1980, 6, 15), nationality="British", biography="History expert."),
    Author(first_name="Ali", last_name="Khan", birth_date=date(1965, 3, 10), nationality="Pakistani", biography="Poet and novelist."),
    Author(first_name="Marie", last_name="Curie", birth_date=date(1867, 11, 7), nationality="Polish", biography="Scientific papers."),
    Author(first_name="Carlos", last_name="Diaz", birth_date=date(1990, 7, 25), nationality="Mexican", biography="Fantasy writer."),
    Author(first_name="Aiko", last_name="Tanaka", birth_date=date(1975, 2, 20), nationality="Japanese", biography="Children’s books."),
    Author(first_name="Emma", last_name="Brown", birth_date=date(1985, 10, 12), nationality="Australian", biography="Biography and non-fiction."),
    Author(first_name="Ivan", last_name="Petrov", birth_date=date(1972, 4, 1), nationality="Russian", biography="Political science expert."),
]
session.add_all(authors)
session.commit()

# Categories
categories = [
    Category(name="Science", description="Science books"),
    Category(name="History", description="History books"),
    Category(name="Fiction", description="Fictional stories"),
    Category(name="Technology", description="Tech manuals"),
    Category(name="Biography", description="Biographical works"),
]
session.add_all(categories)
session.commit()

# Books (3 per library, 5 libraries, total 15)
books = []
for i in range(15):
    books.append(Book(
        library_id=libraries[i % 3].library_id,
        title=f"Book Title {i+1}",
        isbn=f"978-3-16-14841{i%10}",  # Invalid ISBNs on purpose
        publication_date=date(2000+i, 1, 1),
        total_copies=5 + (i % 3),
        available_copies=2 + (i % 3),
    ))
session.add_all(books)
session.commit()

# Book-Author Relations
book_author_links = [
    BookAuthor(book_id=books[i].book_id, author_id=authors[i % len(authors)].author_id)
    for i in range(len(books))
]
session.add_all(book_author_links)
session.commit()

# Book-Category
book_category_links = [
    BookCategory(book_id=books[i].book_id, category_id=categories[i % len(categories)].category_id)
    for i in range(len(books))
]
session.add_all(book_category_links)
session.commit()

# Members
members = []
for i in range(20):
    members.append(Member(
        first_name=f"Member{i+1}".title(),
        last_name=f"Last{i+1}".title(),
        email=f"member{i+1}@mail.com" if i != 3 else "invalid-email.com",
        phone="+91-9876543210" if i % 5 != 0 else "12345678",
        member_type="Student" if i % 2 == 0 else "Faculty",
        registration_date=date(2020, 5, (i % 28 + 1))
    ))
session.add_all(members)
session.commit()

# Borrowings
borrowings = []
for i in range(25):
    borrowings.append(Borrowing(
        book_id=books[i % len(books)].book_id,
        member_id=members[i % len(members)].member_id,
        borrow_date=date(2024, 1, 1),
        due_date=date(2024, 2, 1),
        return_date=date(2024, 1, 30),
        late_fee=0 if i % 3 else 50
    ))
session.add_all(borrowings)
session.commit()

# Reviews (12 entries with some issues)
reviews = []
for i in range(12):
    reviews.append(Review(
        book_id=books[i % len(books)].book_id,
        member_id=members[i % len(members)].member_id,
        rating=5 if i % 4 else 7,  # Invalid rating 7 to test
        comment="Great read!" if i % 2 else "Needs improvement.",
        review_date=date(2024, 3, i+1)
    ))
session.add_all(reviews)
session.commit()

print("Inserted data successfully.")
