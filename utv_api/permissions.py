from rest_framework import permissions

from users.models import CustomUser
from utv_smeta.models import Cards


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user_pk = request.path.split('/')[4]
        user = CustomUser.objects.get(pk=user_pk)
        return bool(request.user == user)


class IsOwnerOrPerformersReadOnly(permissions.BasePermission):
    """Проверка что пользователь является автором карточке или исполнителем"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user in obj.performers.all()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        card_pk = request.path.split('/')[4]
        card = Cards.objects.get(pk=card_pk)
        if request.user in card.performers.all() or request.user is card.author:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class OnlyAuthorOrPerfomance(permissions.BasePermission):
    """Добавлять коментарии может только пользователь закрепленный за карточкой"""
    message = 'Вы не закреплены за карточкой'

    def has_permission(self, request, view):
        card_pk = request.path.split('/')[4]
        card = Cards.objects.get(pk=card_pk)
        if request.user in card.performers.all() or request.user is card.author:
            return True
        return False


class WorkOnlyOne(permissions.BasePermission):
    """Оганичиваем пользователя создавать больше одной работы"""
    message = 'У вас уже есть работа над проектом!'

    def has_permission(self, request, view):
        card_pk = request.path.split('/')[4]
        card = Cards.objects.get(pk=card_pk)
        if 1 == card.worker.filter(author=request.user).count():
            return False
        return True


class OnlyWorkAuthor(permissions.BasePermission):
    message = 'Вы не автор работы'

    def has_permission(self, request, view):
        card_pk = request.path.split('/')[4]
        work_pk = request.path.split('/')[6]
        card = Cards.objects.get(pk=card_pk)
        if request.user == card.worker.get(pk=work_pk).author:
            return True
        return False


class OnlyAuthorCard(permissions.BasePermission):
    message = 'Вы не менеджер проекта'

    def has_permission(self, request, view):
        card_pk = request.path.split('/')[4]
        card = Cards.objects.get(pk=card_pk)
        if request.user == card.author:
            return True
        return False
