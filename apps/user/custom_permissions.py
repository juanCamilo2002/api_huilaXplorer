from rest_framework import permissions


class IsAdminOrIsSelf(permissions.BasePermission):
    """
    Allows access only to administrators or the user themselves.
    """

    def has_object_permission(self, request, view, obj):
        # admin can do anything
        if request.user.is_staff:
            return True

        return obj.id == request.user.id
