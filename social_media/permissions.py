from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method is SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or (request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user
