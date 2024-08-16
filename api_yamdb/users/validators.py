import re

from rest_framework.exceptions import ValidationError

from api_yamdb import settings
from api_yamdb.settings import VALID_CHARS

#TODO check if it's needed
def validate_confirmation_code(code):
    invalid_chars = re.findall(
        VALID_CHARS, code
    )
    if invalid_chars:
        raise ValidationError(
            f'В коде содержатся запрещенные символы: {set(invalid_chars)}'
        )
    return code


def validate_username_symbols(username):
    forbidden_chars = re.findall(r'[^\w.@+-]', username)
    if forbidden_chars:
        raise ValidationError(
            f'В имени содержатся недопустимые символы: {set(forbidden_chars)}'
        )
    return username

def username_is_not_forbidden(username):
    if username in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Имя пользователя {username} не разрешено.'
        )
    return username