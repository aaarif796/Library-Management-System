from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'libraries', LibraryViewSet, basename = 'library')
router.register(r'authors', AuthorViewSet, basename='author')

urlpatterns = [
    path('health/', health_check),
    path('', include(router.urls)),
]
