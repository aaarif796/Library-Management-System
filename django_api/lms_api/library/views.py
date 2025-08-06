from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Library_Col, Author
from .serializers import BookSerializer, LibrarySerializer, AuthorSerializer

@api_view(['GET'])
def health_check(request):
    return Response({"status": "OK"})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library_Col.objects.all()
    serializer_class = LibrarySerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
