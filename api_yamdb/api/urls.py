from django.urls import include, path
from rest_framework import routers
from .views import CommentsViewSet, ReviewsViewSet, CategoryViewSet, \
    GenreViewSet, TitleViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles/(?P<title_id>.+)/reviews', ReviewsViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>.+)/reviews/(?P<review_id>.+)/comments',
    CommentsViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
