from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, CommentSerializer, 
                             ReviewsSerializer)
from reviews.models import Category, Genre, Title, Comments, Reviews
from rest_framework import viewsets
from .permission import IsAuthor


class TitleViewSet(viewsets.ModelViewSet):
    # queryset = Title.objects.annotate(rating=Avg('title_review__score'))
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)
    http_method_names = ['get', 'post', 'patch', 'delete']
    #permission_classes = (IsAdminUser,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    #permission_classes = (IsAdminUser,)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    #permission_classes = (IsAdminUser,)

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
        title = self.get_review_id()
        this_title = Reviews.objects.all()
        if this_title.filter(author=self.request.user):
            raise ValueError('Так нельзя')
        serializer.save(author=self.request.user, title_id=title)

    def perform_update(self, serializer):
        
        super(ReviewsViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        super(ReviewsViewSet, self).perform_destroy(serializer)