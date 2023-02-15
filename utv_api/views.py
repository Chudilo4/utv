from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from utv_smeta.models import *
from utv_api.serializers import UserReadSerializer, CardListSerializers, CardCreateSerializers, CardDetailSerializer, \
    CardDetailUpdateSerializer, CommentCreateSerializers, CommentDetailUpdateSerializer, CommentListSerializers, \
    WorkerListSerializers, WorkerCreateSerializers, WorkerDetailSerializers, TableListSerializers, \
    TableCreateSerializers, TablePlanedUpdateSerializers
from utv_smeta.service import CardService


# Create your views here.


class UsersReadAPIView(APIView):

    def get(self, request, format=None):
        snippets = CustomUser.objects.all()
        serializer = UserReadSerializer(snippets, many=True)
        return Response(serializer.data)


class CardsListAPIView(APIView):
    def get(self, request, format=None):
        data = CardService(author=request.user.pk).my_cards()
        serializer = CardListSerializers(instance=data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CardCreateSerializers(data=request.data)
        if serializer.is_valid():
            CardService(author=request.user.pk, **serializer.data).create_card()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardsDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        card = CardService(card_pk=kwargs['card_pk']).give_me_card()
        serializer = CardDetailSerializer(instance=card)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None):
            return Response({'Ошибка': 'Объект карточки не найден'})
        card = CardService(card_pk=kwargs['card_pk'], **request.data).update_card()
        serializer = CardDetailUpdateSerializer(instance=card, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None):
            return Response({'Ошибка': 'Объект карточки не найден'})
        CardService(card_pk=kwargs['card_pk']).delete_card()
        return Response({'Выполнено': "Карточка удалена"})


class CommentListAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CommentCreateSerializers(data=request.data)
        if serializer.is_valid():
            CardService(author=request.user.pk, card_pk=kwargs['card_pk'], **serializer.data).create_comment()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            comment = CardService(card_pk=kwargs['card_pk'], author=request.user.pk).get_my_comments()
        except Comments.DoesNotExist:
            return Response({'Ошибка': 'Коментарий не найден'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentListSerializers(instance=comment, many=True)
        return Response(serializer.data)


class CommentDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            comment = CardService(card_pk=kwargs['card_pk'], comment_pk=kwargs['com_pk'], author=request.user.pk).my_comment()
        except Comments.DoesNotExist:
            return Response({'Ошибка': 'Коментарий не найден'},status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentDetailUpdateSerializer(instance=comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('com_pk', None):
            return Response({'Ошибка': 'Коментарий не найден'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentDetailUpdateSerializer(data=request.data)
        if serializer.is_valid():
            CardService(card_pk=kwargs['card_pk'], **request.data).create_comment()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('com_pk', None):
            return Response({'Ошибка': 'Объект карточки или коментария не найден'}, status=status.HTTP_400_BAD_REQUEST)
        CardService(comment_pk=kwargs['com_pk'], author=request.user.pk).delete_comment()
        return Response({'Выполнено': "Комментарий удален"}, status=status.HTTP_200_OK)


class WorkerListAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = WorkerCreateSerializers(data=request.data)
        if serializer.is_valid():
            CardService(author=request.user.pk, card_pk=kwargs['card_pk'], **serializer.data).create_worker()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            work = CardService(card_pk=kwargs['card_pk'], author=request.user.pk).get_my_work()
        except Worker.DoesNotExist:
            return Response({'Ошибка': 'Работа не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkerListSerializers(instance=work)
        return Response(serializer.data)


class WorkerDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            worker = CardService(card_pk=kwargs['card_pk'],
                                 author=request.user.pk).get_my_work()
        except Worker.DoesNotExist:
            return Response({'Ошибка': 'Работа не найден'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WorkerListSerializers(instance=worker)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('work_pk', None):
            return Response({'Ошибка': 'Коментарий не найден'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WorkerDetailSerializers(data=request.data)
        if serializer.is_valid():
            CardService(card_pk=kwargs['card_pk'], **request.data).create_worker()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('work_pk', None):
            return Response({'Ошибка': 'Работа не найден'}, status=status.HTTP_400_BAD_REQUEST)
        CardService(card_pk=kwargs['card_pk'], author=request.user.pk).delete_worker()
        return Response({'Выполнено': "Работа удалена"}, status=status.HTTP_200_OK)


class TableListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            tables = CardService(card_pk=kwargs['card_pk']).get_my_tables()
        except TableProject.DoesNotExist:
            return Response({'Таблиц не найдено'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TableListSerializers(instance=tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TableCreateSerializers(data=request.data)
        if serializer.is_valid():
            CardService(author=request.user.pk, card_pk=kwargs['card_pk'], **serializer.data).create_table()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            table = CardService(card_pk=kwargs['card_pk']).get_my_tables()
        except Worker.DoesNotExist:
            return Response({'Ошибка': 'Работа не найден'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TableListSerializers(instance=table, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('table_pk', None):
            return Response({'Ошибка': 'Таблица не найдена'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TablePlanedUpdateSerializers(data=request.data)
        if serializer.is_valid():
            CardService(card_pk=kwargs['card_pk'], table_pk=kwargs['table_pk'], **request.data).update_planned_table()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('table_pk', None):
            return Response({'Ошибка': 'Таблица не найдена'}, status=status.HTTP_400_BAD_REQUEST)
        CardService(card_pk=kwargs['card_pk'], table_pk=kwargs['table_pk']).delete_table()
        return Response({'Выполнено': "Работа удалена"}, status=status.HTTP_200_OK)