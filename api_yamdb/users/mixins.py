from .validators import validate_username_symbols, username_is_not_forbidden


class UserMixin:
    def validate_username(self, username):
        return validate_username_symbols(username_is_not_forbidden(username))
