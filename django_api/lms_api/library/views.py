from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import Book, Library_Col, Author, Member, Borrowing, Review, Category
from .serializers import BookSerializer, LibrarySerializer, AuthorSerializer, MemberSerializer, BorrowingSerializer, ReviewSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "publication_date"]
    ordering_fields = ["title", "total_copies", "publication_date"]
    ordering = ["title"]




class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library_Col.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["campus_location"]
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

    @action(detail=True, methods=["get"], url_path="borrowings")
    def borrowings(self, request, pk=None):
        """
        GET /api/members/{id}/borrowings/
        Returns all borrowing records for this member.
        """
        member = self.get_object()  # ensures 404 if not found
        borrow_qs = Borrowing.objects.filter(member=member)
        page = self.paginate_queryset(borrow_qs)
        if page is not None:
            serializer = BorrowingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BorrowingSerializer(borrow_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



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