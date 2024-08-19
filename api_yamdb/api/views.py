from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, CommentSerializer, 
                             ReviewsSerializer, TitleListSerializer)
from reviews.models import Category, Genre, Title, Comments, Reviews
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from api.pagination import CustomPagination
from rest_framework import status
from rest_framework.response import Response
from api.permissions import IsAuthor, IsAdminOrReadOnly
from django.db.models import Avg
class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    ...

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleSerializer

class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    

class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',) 
    lookup_field = 'slug'

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthor,)

    def get_review_id(self, **kwargs):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, pk=review_id)
        return review

    def get_queryset(self, **kwargs):
        review = self.get_review_id()
        return review.review_comments.all()

    def perform_create(self, serializer):
        review = self.get_review_id()
        serializer.save(author=self.request.user, review_id=review)

    def perform_update(self, serializer):
        super(CommentsViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        super(CommentsViewSet, self).perform_destroy(serializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthor,)

    def get_review_id(self, **kwargs):
        title_id = self.kwargs.get('id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self, **kwargs):
        title = self.get_review_id()
        return title.title_review.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            title = self.get_review_id()
        #this_title = Reviews.objects.all()
        #if this_title.filter(author=self.request.user):
            #raise ValueError('Так нельзя')
            serializer.save(author=self.request.user, title_id=title)

    def perform_update(self, serializer):
        
        super(ReviewsViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        super(ReviewsViewSet, self).perform_destroy(serializer)