from django.shortcuts import render
from django.db import models
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Library_Col, Author, Member, Borrowing, Review, Category
from .serializers import BookSerializer, LibrarySerializer, AuthorSerializer, MemberSerializer, BorrowingSerializer, ReviewSerializer, CategorySerializer, SearchBookSerializer
from django_filters.rest_framework import DjangoFilterBackend


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "publication_date"]
    ordering_fields = ["title", "total_copies", "publication_date"]
    ordering = ["title"]

    @action(detail=True, methods=["get"], url_path= "availability")
    def availability(self, request, pk= None):
        availability_qs = self.get_queryset().filter(available_copies__gt=0)
        page = self.paginate_queryset(availability_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(availability_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods = ['get'], url_path="category")
    def categories(self, request, pk = None):
        category = self.get_object()

    @action(detail= False, methods= ['get'], url_path= 'borrow')
    def borrow(self, request):
        """
            It's display the all the borrowed book with
            /api/books/borrow/
        :param request:
        :return:
        """
        books = Book.objects.all()
        borrow_books = (Borrowing.objects.filter(return_date__isnull=True).select_related('book', 'member'))
        page = self.paginate_queryset(borrow_books)
        if page is not None:
            serializer = BorrowingSerializer(borrow_books, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = BorrowingSerializer(borrow_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods= ['get'], url_path= 'return')
    def return_book(self,request):
        """
            It's return the book which are already returned back to library
            /api/books/return/
        :param request:
        :return:
        """
        return_books = (Borrowing.objects.filter(return_date__isnull = False).select_related('book','member'))
        page = self.paginate_queryset(return_books)
        if page is not None:
            serializer = BorrowingSerializer(return_books, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = BorrowingSerializer(return_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="search")
    def serach_book(self, request):
        """
        It's used to serach the book with the help of title, author name or category
        :param request:
        :return:
        """
        search_query = request.query_params.get('search', '')
        if not search_query:
            return Response(
                {"error": "Please provide a search query parameter"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use the existing search functionality
        books_qs = (self.get_queryset()
                   .filter(
                       models.Q(title__icontains=search_query) |
                       models.Q(authors__first_name__icontains=search_query) |
                       models.Q(authors__last_name__icontains=search_query) |
                       models.Q(categories__name__icontains=search_query)
                   ).distinct())
        page = self.paginate_queryset(books_qs)
        if page is not None:
            serializer = SearchBookSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = SearchBookSerializer(books_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []
    ordering = []


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
        member = self.get_object()
        borrow_qs = Borrowing.objects.filter(member=member)
        page = self.paginate_queryset(borrow_qs)
        if page is not None:
            serializer = BorrowingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BorrowingSerializer(borrow_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []
    search_fields = ['member__first_name']
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

# class SearchBookView(viewsets.ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = SearchBookSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'authors__first_name', 'authors__last_name','categories__name']


class StatisticsView(APIView):
    def get(self, request):
        data = {
            "total_books": Book.objects.count(),
            "total_members": Member.objects.count(),
            "books_borrowed": Borrowing.objects.count(),
            "books_available": Book.objects.filter(available_copies__gt=0).count(),
        }
        return Response(data, status=status.HTTP_200_OK)

