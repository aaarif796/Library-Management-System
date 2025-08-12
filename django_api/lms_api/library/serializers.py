from django.core.validators import EmailValidator, RegexValidator
from rest_framework import serializers
from .models import Book, Library_Col, Author, Category, Member, Review, Borrowing
from django.utils import timezone

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Col
        fields = '__all__'

    def validate_l_name(self, value):
        return value.strip().title()

    def validate_contact_email(self, value):
        value = value.strip().lower()
        EmailValidator()(value)
        return value

    def validate_campus_location(self, value):
        return value.strip().title()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def validate_first_name(self, value):
        return value.capitalize()

    def validate_last_name(self, value):
        return value.capitalize()

    def validate_nationality(self, value):
        return value.capitalize()

class BookSerializer(serializers.ModelSerializer):
    library_name = serializers.CharField(source="library.l_name", read_only = True)
    class Meta:
        model = Book
        fields = '__all__'

    def validate_title(self, value):
        return value.strip().title()

    def validate_isbn(self, value):
        isbn = value.replace("-", "").replace(" ","")
        if len(isbn) not in [10,13]:
            raise serializers.ValidationError("Must be 10 or 13")
        if not isbn.isdigit():
            raise serializers.ValidationError("Must be digits")
        return isbn

    def validate_publication_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Enter the correct publication date")
        return value

    def validate_total_copies(self, value):
        if value<0:
            raise serializers.ValidationError("Enter the correct total copies")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        return value.strip().title()


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.CharField(source = "member.first_name")
    book_title = serializers.CharField(source= "book.title")
    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 to 5")
        return value


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def validate_first_name(self, value):
        return value.strip().capitalize()

    def validate_last_name(self, value):
        return value.strip().capitalize() if value else value

    def validate_email(self, value):
        value = value.strip().lower()
        EmailValidator()(value)
        return value.strip()

    def validate_phone(self, value):
        phone = value.strip().replace(" ", "").replace("-", "")
        if not phone.startswith("+"):
            phone = "+91" + phone  # default country code
        return phone

    def validate_member_type(self, value):
        contains = ('Student', 'Faculty','Guest')
        if value.strip().capitalize() in contains:
            return value
        else:
            raise serializers.ValidationError("It must be any of these: ('Student', 'Faculty','Guest')")

    def validate_registration_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Enter the correct date")
        return value



class BorrowingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    class Meta:
        model = Borrowing
        fields = '__all__'

    def validate(self, data):
        if data.get("due_date") and data['due_date'] < data['borrow_date']:
            raise serializers.ValidationError("Due date must be after borrow date")

        if data.get("due_date") and data['return_date']<data['due_date']:
            raise serializers.ValidationError("Enter the correct due date")

        return data


class SearchBookSerializer(serializers.ModelSerializer):
    author_names = serializers.SerializerMethodField(read_only=True)
    category_names = serializers.SerializerMethodField(read_only=True)
    l_name = serializers.CharField(source= 'library.l_name',read_only= True)
    class Meta:
        model = Book
        fields = ['title','isbn','l_name','author_names','category_names']

    def get_author_names(self, obj):
        # returns list of first names
        return [a.first_name+" "+a.last_name for a in obj.authors.all()]

    def get_category_names(self, obj):
        return [c.name for c in obj.categories.all()]

class BookMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='member.first_name', read_only=True)
    last_name = serializers.CharField(source='member.last_name', read_only=True)
    b_date = serializers.CharField(source='borrow_date', read_only=True)
    l_name = serializers.CharField(source='book.library.l_name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            'first_name', 'last_name', 'b_date',
            'l_name', 'book_title', 'book_isbn'
        ]