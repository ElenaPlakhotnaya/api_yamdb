from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated:
                if (
                    request.user.is_superuser or request.user.is_admin
                    ):
                    return True
        return False
