from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows access only to post owner, or is a read-only request.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(view) == 'UserDetailView':
            return obj == request.user