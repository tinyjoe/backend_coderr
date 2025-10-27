from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Allows access only to users of type 'business'.
    """
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.customuser.type == 'business')
    

class IsAuthenticatedOrCustomerUser(permissions.BasePermission):
    """
    Permissions: 
    GET: Any authenticated user.
    POST/PATCH: Only users of type 'customer'.
    DELETE: Only staff users.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == 'GET':
            return True
        if request.method == 'DELETE':
            return True
        if request.method in ['POST', 'PATCH', 'PUT']:
            if hasattr(request.user, 'customuser') and getattr(request.user.customuser, 'type', None) == 'customer':
                return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_staff
        return True