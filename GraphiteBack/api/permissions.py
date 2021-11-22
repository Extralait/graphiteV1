from rest_framework.permissions import BasePermission


class NoBody(BasePermission):
    """
    Никто не имеет доступ
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
