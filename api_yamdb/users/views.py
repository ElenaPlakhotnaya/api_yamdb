from sqlite3 import IntegrityError

from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from api_yamdb import settings
from users.models import User
from users.permissions import IsAdmin
from users.serializers import UserSerializer, UserNotAdminSerializer, \
    RetrieveTokenSerializer, SignUpSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'email')
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data,
                            status=status.HTTP_200_OK)
        serializer = UserNotAdminSerializer(request.user, data=request.data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetTokenView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(self, request):
        serializer = RetrieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        user.save()
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ApiUserSignupView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
        send_mail(
            f'Код подтверждения регистрации {user.first_name}',
            f'Ваш код подтверждения: {user.confirmation_code}',
            f'{settings.ADMIN_EMAIL_ADDRESS}',
            [email]
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
