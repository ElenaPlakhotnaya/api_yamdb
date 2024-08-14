from django.shortcuts import render
from rest_framework import filters

from reviews.models import Titles, Categories, Genres

from api.serializers import TitleSerializer, CategorySerializer, GenreSerializer

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    