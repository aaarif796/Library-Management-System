from django.core.validators import EmailValidator
from rest_framework import serializers
from .models import Book, Library_Col, Author, Category, Member, Review, Borrowing

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Col
        fields = '__all__'

    def validate_l_name(self, value):
        return value.strip().title()

    def validate_contact_email(self, value):
        EmailValidator()(value)
        return value.lower()

    def validate_campus_location(self, value):
        return value.strip().title()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def validate_first_name(self, value):
        return value.capatilize()

    def validate_last_name(self, value):
        return value.capatilize()

    def validate_nationality(self, value):
        return value.capatilize()

class BookSerializer(serializers.ModelSerializer):
    library_name = serializers.CharField(source="library.l_name", read_only = True)
    class Meta:
        model = Book
        fields = '__all__'

    def validate_title(self, value):
        return value.title()

    def validate_isbn(self, value):
        pass

    def validate_publication_date(self, value):
        pass

    def validate_total_copies(self, value):
        pass


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        pass


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.CharField(source = "member.first_name")
    book_title = serializers.CharField(source= "book.title")
    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        pass


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def validate_first_name(self, value):
        pass

    def validate_last_name(self, value):
        pass

    def validate_email(self, value):
        pass

    def validate_phone(self, value):
        pass

    def validate_member_type(self, value):
        pass

    def validate_registration_date(self, value):
        pass



class BorrowingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    class Meta:
        model = Borrowing
        fields = '__all__'

    def validate_due_date(self, value):
        pass

    def validate_return_date(self, value):
        pass

    def validate_late_fee(self, value):
        pass



class SearchBookSerializer(serializers.ModelSerializer):
    author_names = serializers.SerializerMethodField()
    category_names = serializers.SerializerMethodField()
    l_name = serializers.CharField(source= 'library.l_name',read_only= True)
    class Meta:
        model = Book
        fields = ['title','isbn','l_name','author_names','category_names']
    def get_author_names(self, obj):
        # returns list of first names
        return [a.first_name+" "+a.last_name for a in obj.authors.all()]

    def get_category_names(self, obj):
        return [c.name for c in obj.categories.all()]