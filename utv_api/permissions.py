from rest_framework import permissions

from utv_api.models import Cards


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False


class IsOwnerCardOrReadPerformers(IsAuthor):
    def has_permission(self, request, view):
        card = Cards.objects.get(pk=view.kwargs['card_pk'])
        if request.user in card.performers.all():
            return True
        return False


