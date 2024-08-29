from rest_framework import permissions

class IsSelfReview(permissions.BasePermission):
    """
    Allows access only to the user themselves
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id