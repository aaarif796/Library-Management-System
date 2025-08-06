from rest_framework import serializers
from .models import Book, Library_Col, Author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Col
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

