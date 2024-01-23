from rest_framework import permissions


class IsOriginalUser(permissions.BasePermission):
    """
    Custom permission to allow only the original user to edit or delete a post.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the original user who created the post.
        return obj.user == request.user
