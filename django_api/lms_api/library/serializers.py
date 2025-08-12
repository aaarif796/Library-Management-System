from rest_framework import serializers
from .models import Book, Library_Col, Author, Category, Member, Review, Borrowing

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Col
        fields = '__all__'

    def validate_l_name(self, value):
        return value.strip().title()

    def validate_contact_email(self):
        

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    library_name = serializers.CharField(source="library.l_name", read_only = True)
    class Meta:
        model = Book
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.CharField(source = "member.first_name")
    book_title = serializers.CharField(source= "book.title")
    class Meta:
        model = Review
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class BorrowingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    class Meta:
        model = Borrowing
        fields = '__all__'

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