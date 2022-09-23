from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if str(view) == 'CommentDetailView':
            return obj.comment_author == request.user

        if str(view) == 'PostDetailView':
            return obj.post_author == request.user