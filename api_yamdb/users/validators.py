import re

from django.conf import settings
from rest_framework.exceptions import ValidationError


def validate_username(value):
    forbidden_chars = re.findall(r'[^\w.@+-]', value)
    if forbidden_chars:
        raise ValidationError(
            f'В имени содержатся недопустимые следующие символы: '
            f'{set(forbidden_chars)}'
        )
    return value


def validate_username_is_forbidden(value):
    if value in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Недопустимое имя пользователя: {value}'
        )
    return value
