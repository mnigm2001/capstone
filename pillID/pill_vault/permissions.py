from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow delete if the user is an admin
        if request.user and request.user.is_staff:
            return True

        # Allow delete only if the user is the owner of the account
        return obj == request.user
