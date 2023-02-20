from rest_framework import permissions

from users.models import CustomUser
from utv_smeta.models import Cards


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.pk == obj.pk)


class IsOwnerOrPerformersReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        print(request)
        return obj.author == request.user or request.user in obj.performers.all()
