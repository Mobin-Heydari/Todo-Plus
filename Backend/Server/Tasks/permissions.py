from rest_framework.permissions import BasePermission


class IsTheTaksOwner(BasePermission):
    """
    Custom permission for The task owner
    """
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False