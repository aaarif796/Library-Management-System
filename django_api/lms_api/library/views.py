from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import models
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Library_Col, Author, Member, Borrowing, Review, Category
from .serializers import BookSerializer, LibrarySerializer, AuthorSerializer, MemberSerializer, BorrowingSerializer, ReviewSerializer, CategorySerializer, SearchBookSerializer, BookMemberSerializer
from django_filters.rest_framework import DjangoFilterBackend
from datetime import timedelta
from django.utils import timezone

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "publication_date"]
    ordering_fields = ["title", "total_copies", "publication_date"]
    ordering = ["title"]

    @action(detail=True, methods=["get"], url_path= "availability")
    def availability(self, request, pk= None):
        """
            Check the book availability with are available or not by passing the book id
        """
        availability_qs = self.get_queryset().filter(id = pk, available_copies__gt=0)
        page = self.paginate_queryset(availability_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(availability_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="category")
    def categories(self, request):
        """
        Retrieve books of a specific category that are available.
        Example: /api/books/category/?name=Programming
        """
        category_name = request.query_params.get("name")
        if not category_name:
            return Response(
                {"error": "Category name is required in query param ?name="},
                status=status.HTTP_400_BAD_REQUEST
            )

        books = self.get_queryset().filter(
            categories__name__iexact=category_name,
            available_copies__gt=0
        )

        page = self.paginate_queryset(books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        api/books/search/?search=clean%20code
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


    @action(detail=True, methods=["post"], url_path="borrow-book")
    def borrow_book(self, request, pk=None):
        """
        API to borrow a book.
        Expects: member_id (required), due_date (optional, ISO string, default 14 days)
        """
        # Get book (DRF will 404 automatically if not found)
        book = self.get_object()

        # Check available copies
        if book.available_copies <= 0:
            return Response({"error": "No available copies for this book"}, status=status.HTTP_400_BAD_REQUEST)

        # Get member id from request
        member_id = request.data.get("member_id")
        if not member_id:
            return Response({"error": "member_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check member exists
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if this member already has this book borrowed and not returned
        if Borrowing.objects.filter(member=member, book=book, return_date__isnull=True).exists():
            return Response({"error": "Book is already borrowed by this member"}, status=status.HTTP_400_BAD_REQUEST)

        # Reduce available copies
        book.available_copies -= 1
        book.save()

        # Set borrow and due date
        borrow_date = timezone.now()
        due_date_str = request.data.get("due_date")
        if due_date_str:
            due_date = parse_datetime(due_date_str)
            if timezone.is_naive(due_date):
                due_date = timezone.make_aware(due_date)
        else:
            due_date = borrow_date + timedelta(days=14)

        # Create borrowing record
        borrowing = Borrowing.objects.create(
            member=member,
            book=book,
            borrow_date=borrow_date,
            due_date=due_date,
            late_fee=0,
            return_date=None
        )

        return Response({
            "message": "Book borrowed successfully",
            "book": book.title,
            "borrow_id": borrowing.id,
            "due_date": due_date
        }, status=status.HTTP_201_CREATED)

    # Return book api
    @action(detail=True, methods=["post"], url_path="return-book")
    def return_book_action(self, request, pk=None):
        """
        API to return a borrowed book.
        Increases available_copies by 1.
        Calculates late fee if returned after due_date.
        Expects: member_id (required)
        """
        member_id = request.data.get("member_id")
        if not member_id:
            return Response({"error": "member_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            borrowing = Borrowing.objects.get(
                member=member, 
                book_id=pk,
                return_date__isnull=True
            )
        except Borrowing.DoesNotExist:
            return Response({"error": "No active borrowing record found"}, status=status.HTTP_404_NOT_FOUND)

        # Return date
        return_date = timezone.now()
        borrowing.return_date = return_date

        # Calculate late fee
        late_days = (return_date.date() - borrowing.due_date.date()).days
        if late_days > 0:
            borrowing.late_fee = late_days * 10  # Rs 10 per day late
        else:
            borrowing.late_fee = 0

        borrowing.save()

        # Increase available copies
        borrowing.book.available_copies += 1
        borrowing.book.save()

        return Response({
            "message": "Book returned successfully",
            "late_fee": borrowing.late_fee
        }, status=status.HTTP_200_OK)


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
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = []
    # search_fields = []
    # ordering_fields = []
    # ordering = []


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
            serializer = BookMemberSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BookMemberSerializer(borrow_qs, many=True)
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
    @swagger_auto_schema(
        operation_summary="Retrieve library statistics",
        operation_description=(
            "Returns statistical information about the library, "
            "including total number of books, members, borrowed books, "
            "and books currently available."
        ),
        responses={
            200: openapi.Response(
                description="Statistics retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "total_books": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total number of books in the library"
                        ),
                        "total_members": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total registered members"
                        ),
                        "books_borrowed": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Number of borrowed books"
                        ),
                        "books_available": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Number of books currently available"
                        )
                    }
                ),
                examples={
                    "application/json": {
                        "total_books": 120,
                        "total_members": 45,
                        "books_borrowed": 30,
                        "books_available": 90
                    }
                }
            )
        }
    )
    def get(self, request):
        data = {
            "total_books": Book.objects.count(),
            "total_members": Member.objects.count(),
            "books_borrowed": Borrowing.objects.count(),
            "books_available": Book.objects.filter(available_copies__gt=0).count(),
        }
        return Response(data, status=status.HTTP_200_OK)