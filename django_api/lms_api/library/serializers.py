from rest_framework import serializers
from .models import Book, Library_Col, Author, Category, Member, Review, Borrowing

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Col
        fields = '__all__'

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
    author_fname = serializers.CharField(source='authors.first_name', read_only= True)
    author_lname = serializers.CharField(source='authors.last_name', read_only= True)
    b_category = serializers.CharField(source='categories.name', read_only= True)
    l_name = serializers.CharField(source= 'library.l_name',read_only= True)
    class Meta:
        model = Book
        fields = ['title','isbn','l_name','author_fname','author_lname', 'b_category']
