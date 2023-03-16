from rest_framework import permissions


class IsOwnerOrPerformersReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user in obj.performers.all() or request.user == obj.author:
            return True
        return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False


class AuthorOrPerformersEvent(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user in obj.performers.all() or request.user == obj.author:
            return True
        return False
