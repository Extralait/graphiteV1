from rest_framework.permissions import BasePermission


class AuctionOwnerOrAdmin(BasePermission):
    """
    Владелец или администратор
    """

    def has_object_permission(self, request, view, obj):
        return (obj.drop.owner == request.user) or request.user.is_staff


