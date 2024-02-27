from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):

    def __init__(self, *permissions):
        self.permissions = permissions

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.has_perms(self.permissions)
        )
