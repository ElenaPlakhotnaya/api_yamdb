from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
