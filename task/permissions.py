from rest_framework import permissions


class IsAdminCreateOrUserTaskUpdateOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if request.method == "POST":
            return False 

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_superuser:
            return True

        return obj.user == request.user