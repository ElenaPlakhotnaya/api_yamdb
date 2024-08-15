from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import CommentSerializer, ReviewsSerializer
from reviews.models import Comments, Reviews, Titles


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def get_review_id(self, **kwargs):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, pk=review_id)
        return review

    def get_queryset(self, **kwargs):
        review = self.get_review_id()
        return review.comments.all()

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

    def get_review_id(self, **kwargs):
        title_id = self.kwargs.get('id')
        title = get_object_or_404(Titles, pk=title_id)
        return title

    def get_queryset(self, **kwargs):
        title = self.get_review_id()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_review_id()
        serializer.save(author=self.request.user, title_id=title)

    def perform_update(self, serializer):
        super(ReviewsViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        super(ReviewsViewSet, self).perform_destroy(serializer)

