from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings
from users.permissions import IsAdmin
from users.serializers import (AuthSerializer, UserAccessTokenSerializer,
                               UserNotAdminSerializer, UserSerializer)

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
            methods=['GET'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(UserSerializer(request.user).data,
                        status=status.HTTP_200_OK)

    @me.mapping.patch
    def me_patch(self, request):
        serializer = UserNotAdminSerializer(request.user,
                                            data=request.data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class APIGetTokenView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        token = AccessToken.for_user(user)
        return Response({'token': str(token)},
                        status=status.HTTP_200_OK)


class ApiUserSignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=request.data.get('username'),
                email=request.data.get('email')
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код подтверждения',
                f'Ваш код - {confirmation_code}',
                settings.ADMIN_EMAIL_ADDRESS,
                [request.data.get('email')]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
