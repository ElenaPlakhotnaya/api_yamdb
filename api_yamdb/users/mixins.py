from .validators import username_is_not_forbidden, validate_username_symbols


class UserMixin:
    def validate_username(self, username):
        return validate_username_symbols(username_is_not_forbidden(username))
