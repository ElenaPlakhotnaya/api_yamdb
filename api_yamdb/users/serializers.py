from rest_framework import serializers

from api_yamdb.settings import CONF_CODE_MAX_LEN
from users.models import User

from .constants import MAX_LENGTH_EMAIL, MAX_LENGTH_NAME
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


class SignUpSerializer(serializers.Serializer, UserMixin):
    username = serializers.CharField(required=True, max_length=MAX_LENGTH_NAME)
    email = serializers.EmailField(required=True, max_length=MAX_LENGTH_EMAIL)


class UserNotAdminSerializer(serializers.ModelSerializer, UserMixin):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
