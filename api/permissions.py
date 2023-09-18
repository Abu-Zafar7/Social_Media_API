from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any user (GET, HEAD, OPTIONS requests)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the post
        return obj.user == request.user

class IsLikedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for any user (GET, HEAD, OPTIONS requests)
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated