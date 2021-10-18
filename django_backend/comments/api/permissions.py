from rest_framework.permissions import BasePermission

class IsObjectOwner(BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.user.id:
            return True
        return False
