from rest_framework import permissions


class IsAdmin(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                or request.method in permissions.SAFE_METHODS)


class IsAdminOrModeratorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
        )
