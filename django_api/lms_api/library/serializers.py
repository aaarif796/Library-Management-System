from rest_framework import serializers
from .models import Book, Library_Col, Author, BookAuthor, BookCategory, Category, Member, Review, Borrowing

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Col
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    library_name = serializers.CharField(source='library.l_name', read_only=True)
    categories = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['book_id','library_name','categories']
        # fields = ["book_id","library_name", 'title','isbn','publication_date','total_copies','available_copies', 'library_id']
        # fields = '__all__'

    def get_categories(self, obj):
        try:
            # Filter BookCategory objects directly
            book_categories = BookCategory.objects.filter(book_id=obj.book_id)
            return [bc.category.name for bc in book_categories]
        except:
            return []
    # def get_categories(self, obj):
    #     return [bc.category.name for bc in obj.bookcategory_set.all()]

class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields= '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'



