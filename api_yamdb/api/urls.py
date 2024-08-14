from django.urls import include, path
from rest_framework import routers
from .views import CommentsViewSet, ReviewsViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'titles/(?P<id>.+)/reviews', ReviewsViewSet)
router_v1.register(r'titles/(?P<id>.+)/reviews/(?P<review_id>.+)/comments', CommentsViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]