from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'libraries', LibraryViewSet, basename = 'library')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'members',MemberViewSet, basename='member')
router.register(r'reviews',ReviewViewSet, basename='review')
router.register(r'borrowings',BorrowingViewSet, basename='borrowing')

urlpatterns = [
    path('', include(router.urls)),
]
