from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
 
from users.models import User

from .constants import MAX_LENGTH_EMAIL, MAX_LENGTH_NAME
from .mixins import UserMixin


class UserAccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data


class UserSerializer(serializers.ModelSerializer, UserMixin):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserNotAdminSerializer(serializers.ModelSerializer, UserMixin):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class AuthSerializer(serializers.Serializer, UserMixin):
    username = serializers.CharField(required=True, max_length=MAX_LENGTH_NAME)
    email = serializers.EmailField(required=True, max_length=MAX_LENGTH_EMAIL)

    def validate(self, data):
        try:
            User.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Одно из полей username или email уже занято'
            )
        return data
