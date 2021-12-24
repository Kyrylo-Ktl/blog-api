"""Module with custom permissions"""

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    """
    Allows only read access.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsAuthorUser(IsAuthenticated):
    """
    Allows access only to author.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminUser(IsAuthenticated):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(
            super().has_permission(request, view) and
            request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
