import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api_yamdb.settings import CONF_CODE_MAX_LEN, VALID_CHARS, DEFAULT_CONF_CODE
from users.models import User

from .constants import MAX_LENGTH_NAME, MAX_LENGTH_EMAIL
from .mixins import UserMixin
from .validators import validate_confirmation_code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class RetrieveTokenSerializer(serializers.Serializer, UserMixin):
    username = serializers.CharField(required=True, max_length=MAX_LENGTH_NAME)
    confirmation_code = serializers.CharField(required=True,
                                              max_length=CONF_CODE_MAX_LEN,
                                              validators=(
                                                  validate_confirmation_code,)
                                              )

    def validate_confirmation_code(self, pin_code):
        if pin_code == DEFAULT_CONF_CODE:
            raise ValidationError(
                'Ошибка. Сначала получите код подтверждения.'
            )
        invalid_chars = re.findall(
            fr"'{re.escape(VALID_CHARS)}\s'", pin_code
        )
        if invalid_chars:
            raise ValidationError(
                f'Код не должен содержать символы {invalid_chars}'
            )
        return pin_code


class SignUpSerializer(serializers.Serializer, UserMixin):
    username = serializers.CharField(required=True, max_length=MAX_LENGTH_NAME)
    email = serializers.EmailField(required=True, max_length=MAX_LENGTH_EMAIL)


class UserNotAdminSerializer(serializers.ModelSerializer, UserMixin):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
