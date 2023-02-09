from rest_framework import permissions


class EsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='editores'):
            return True
        return False