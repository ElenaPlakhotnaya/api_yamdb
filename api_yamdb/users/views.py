import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from users.permissions import IsAdmin
from users.serializers import UserSerializer, UserNotAdminSerializer, \
    RetrieveTokenSerializer, SignUpSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'email')
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False,
            methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated],
            url_path='me')
    def me(self, request):
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data,
                            status=status.HTTP_200_OK)
        serializer = UserNotAdminSerializer(request.user,
                                            data=request.data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RetrieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_200_OK)
        user.save()
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ApiUserSignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data)
        except IntegrityError:
            raise ValidationError(
                'Пользователь с таким {} уже зарегистрирован.'.format(
                    'email' if User.objects.filter(email=email) else 'именем')
            )
        user.confirmation_code = ''.join(
            random.choices(string.ascii_uppercase + string.digits,
                           k=settings.CONF_CODE_MAX_LEN))
        user.save()
        send_mail(
            f'Код подтверждения регистрации {user.first_name}',
            f'Ваш код подтверждения: {user.confirmation_code}',
            f'{settings.ADMIN_EMAIL_ADDRESS}',
            [email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
