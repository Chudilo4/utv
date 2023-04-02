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


class IsOwnerCardOrReadPerformers(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        elif request.user in obj.performers.all():
            if request.method in permissions.SAFE_METHODS:
                return True
        else:
            return False


class OnlyPerformers(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        card = Cards.objects.get(pk=view.kwargs['card_pk'])
        if request.user == card.author or request.user in card.performers.all():
            return True
        return False


class OnlyAuthorCard(permissions.BasePermission):
    def has_permission(self, request, view):
        card = Cards.objects.get(pk=view.kwargs['card_pk'])
        if request.user == card.author:
            return True
        return False
