from rest_framework import permissions

from utv_api.models import CustomUser, Event
from utv_api.models import Cards


def get_or_none(obj, pk):
    try:
        o = obj.objects.get(pk=pk)
    except obj.DoesNotExist:
        return None
    return o


class IsOwnerOrPerformersReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        card_pk = request.path.split('/')[4]
        card = get_or_none(Cards, card_pk)
        if card:
            if request.user in card.performers.all() or request.user == card.author:
                return True
        return False


class IsOwnerCard(permissions.BasePermission):
    def has_permission(self, request, view):
        card_pk = request.path.split('/')[4]
        card = get_or_none(Cards, card_pk)
        if card:
            if request.user == card.author:
                return True
        return False


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user_pk = request.path.split('/')[4]
        user = get_or_none(CustomUser, user_pk)
        if user:
            if request.user == user:
                return True
        return False


class AuthorOrPerformersEvent(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     event_pk = request.path.split('/')[4]
    #     event = get_or_none(Event, event_pk)
    #     if event:
    #         if request.user in event.performers.all() or request.user == event.author:
    #             return True
    #     return False

    def has_object_permission(self, request, view, obj):
        if request.user in obj.performers.all() or request.user == obj.author:
            return True
        return False
