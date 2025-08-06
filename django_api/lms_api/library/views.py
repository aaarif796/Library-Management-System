from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


@api_view(['GET'])
def health_check(request):
    return Response({"status": "OK"})

class BookViewSet(viewsets.ReadOnlyModelViewSet):  # Only GET (list and retrieve)
    queryset = Book.objects.all()
    serializer_class = BookSerializer

