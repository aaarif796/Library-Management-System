import factory
from django.utils import timezone
from ..models import Library_Col, Author, Category, Book, Member, Borrowing, Review

class LibraryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Library_Col
    l_name = factory.Faker("company")
    campus_location = factory.Faker("city")
    contact_email = factory.Faker("email")
    phone_number = "+911234567890"

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker("date_of_birth")
    nationality = factory.Faker("country")

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker("word")
    description = factory.Faker("sentence")

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    library = factory.SubFactory(LibraryFactory)
    title = factory.Faker("sentence", nb_words=3)
    isbn = "1234567890"
    publication_date = factory.LazyFunction(lambda: timezone.now())
    total_copies = 5
    available_copies = 5

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for author in extracted:
                self.authors.add(author)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)

class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = "+911234567890"
    member_type = "Student"
    registration_date = factory.LazyFunction(lambda: timezone.now())

class BorrowingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Borrowing
    member = factory.SubFactory(MemberFactory)
    book = factory.SubFactory(BookFactory)
    borrow_date = factory.LazyFunction(lambda: timezone.now())
    due_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=14))
    return_date = None
    late_fee = 0

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review
    member = factory.SubFactory(MemberFactory)
    book = factory.SubFactory(BookFactory)
    rating = 4
    comments = factory.Faker("sentence")
    review_data = "2025-08-14"