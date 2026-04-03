from rest_framework.permissions import BasePermission
from apps.users.models import Role

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == Role.ADMIN)


class IsAnalystOrAdmin(BasePermission):

    message = "Only analysts and administrators can access this resource"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [Role.ANALYST, Role.ADMIN]
        )

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return request.user.is_authenticated
        return request.user.role == Role.ADMIN