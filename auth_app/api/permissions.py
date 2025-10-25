from rest_framework import permissions

class IsAuthenticatedOrOwnProfile(permissions.BasePermission):
    """
    For GET requests: Allows access to authenticated users.
    For POST: Allows access only to the owner of the profile.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return obj.user == request.user