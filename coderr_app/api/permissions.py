from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Allows access only to users of type 'business'.
    """
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.customuser.type == 'business')