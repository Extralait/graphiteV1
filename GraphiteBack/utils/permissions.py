from rest_framework.permissions import BasePermission


class Nobody(BasePermission):
    """
    Никто не имеет доступ
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class OwnerOrAdmin(BasePermission):
    """
    Владелец или администратор
    """

    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user) or request.user.is_staff


class AddresseeOrAdmin(BasePermission):
    """
    Адресат или администратор
    """

    def has_object_permission(self, request, view, obj):
        return (obj.to_user == request.user) or request.user.is_staff


class ParticipantsOrAdmin(BasePermission):
    """
    Участники сделки
    """

    def has_object_permission(self, request, view, obj):
        return (request.user in [obj.owner,obj.buyer]) or request.user.is_staff
