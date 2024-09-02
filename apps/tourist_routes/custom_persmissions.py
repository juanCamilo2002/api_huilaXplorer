from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Allows access only to the user themselves
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user