from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet, ApiUserSignupView, APIGetTokenView

api_v1_router = routers.DefaultRouter()
api_v1_router.register(r'users', UserViewSet, basename='get_token')

auth = [
    path('signup/', ApiUserSignupView.as_view(), name='register'),
    path('token/', APIGetTokenView.as_view(), name='token')
]
urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
    path('v1/auth/', include(auth))

]
