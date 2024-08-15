import re

from django.conf import settings
from pytest_django.fixtures import settings
from rest_framework import serializers

from api_yamdb.settings import CONF_CODE_MAX_LEN, VALID_CHARS
from users.models import User

from .constants import MAX_LENGTH_NAME, MAX_LENGTH_EMAIL
from .validators import validate_confirmation_code




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class RetrieveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True, max_length=MAX_LENGTH_NAME)
    confirmation_code = serializers.CharField(required=True,
                                              max_length=CONF_CODE_MAX_LEN,
                                              validators=(
                                                  validate_confirmation_code,)
                                              )

    @staticmethod
    def validate_confirmation_code(self, value):
        if value == settings.DEFAULT_CONF_CODE:
            raise serializers.ValidationError(
                'Ошибка! Необходимо получить код подтверждения!'
            )
        invalid_chars = re.findall(
            VALID_CHARS, value
        )
        if invalid_chars:
            raise serializers.ValidationError(
                f'В коде содержатся запрещенные символы: {set(invalid_chars)}'
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=MAX_LENGTH_NAME)
    email = serializers.EmailField(required=True, max_length=MAX_LENGTH_EMAIL)


class UserNotAdminSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
