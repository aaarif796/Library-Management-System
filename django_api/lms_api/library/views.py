from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Library_Col, Author, Member, Borrowing, Review, Category
from .serializers import BookSerializer, LibrarySerializer, AuthorSerializer, MemberSerializer, BorrowingSerializer, ReviewSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["book_id", "title", "publication_date"]
    search_fields = ["bookcategory__category__name", "bookauthor__author__first_name","title"]
    ordering_fields = ["title", "total_copies", "publication_date"]
    ordering = ["title"]

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library_Col.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["library_id", "campus_location"]
    search_fields = ["l_name", "campus_location"]
    ordering_fields = ["l_name", "campus_location"]
    ordering = ["l_name"]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["first_name", "nationality"]
    search_fields = ["first_name", "nationality"]
    ordering_fields = ["first_name","nationality"]
    ordering = ["first_name"]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["first_name", "member_type"]
    search_fields = ["first_name", "member_type"]
    ordering_fields = ["first_name"]
    ordering = ["first_name"]


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []
    ordering = []


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []
    ordering = []


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]