from rest_framework import permissions


class IsAuthorOrArmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.method in permissions.SAFE_METHODS):
            return False
        if not request.user.is_authenticated:
            return False
        if not (request.user.is_superuser or request.user.is_admin):
            return False
        return True
