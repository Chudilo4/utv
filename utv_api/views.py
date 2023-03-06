import logging

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service_app.service import (
    CardService,
    CommentService,
    WorkerService,
    TableService,
    create_excel,
    get_my_excel_table)
from utv_api.models import CustomUser
from utv_api.permissions import IsOwnerOrPerformersReadOnly, IsOwnerCard, IsUser
from utv_api.serializers import (
    UserReadSerializer,
    CardListSerializers,
    CardCreateSerializers,
    CardDetailSerializer,
    CardDetailUpdateSerializer,
    CommentCreateSerializers,
    CommentDetailUpdateSerializer,
    CommentListSerializers,
    WorkerListSerializers,
    WorkerCreateSerializers,
    WorkerDetailSerializers,
    TableListSerializers,
    TableCreateSerializers,
    UserCreateSerializers,
    UserDetailSerializers,
    TableUpdatePlannedSerializers,
    TableUpdateFactSerializers, ExcelSerializer, ExcelCreateSerializer)
from utv_api.models import Comments, Worker, TableProject
from django.utils import timezone

logger = logging.getLogger(__name__)


class UsersReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        snippets = CustomUser.objects.all()
        serializer = UserReadSerializer(snippets, many=True, context={'request': request})
        logger.info(f'{timezone.now()} {request.user} получил список пользователей')
        return Response(serializer.data, status.HTTP_200_OK)


class UserRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializers(data=request.data)
        if serializer.is_valid():
            avatar = request.data['avatar']
            user = CustomUser.objects.create(username=request.data['username'],
                                             first_name=request.data['first_name'],
                                             last_name=request.data['last_name'],
                                             avatar=avatar
                                             )
            user.set_password(request.data['password'])
            user.save()
            serializer2 = UserReadSerializer(instance=user)
            logger.info(f'{timezone.now()} Зарегестрировался новый пользователь')
            return Response(serializer2.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [IsUser]

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs['user_pk'])
        serializer = UserReadSerializer(user)
        logger.info(f'{timezone.now()} {request.user} обратился к своему профилю')
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs['user_pk'])
        serializer = UserDetailSerializers(data=request.data)
        if serializer.is_valid():
            avatar = request.data['avatar']
            user.username = request.data['username']
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.set_password(request.data['password'])
            user.avatar.delete(save=False)
            user.avatar = avatar
            user.save()
            logger.info(f'{timezone.now()} {request.user} поменял свой профиль')
            serializer2 = UserReadSerializer(instance=user)
            return Response(serializer2.data, status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs['user_pk'])
        user.delete()
        logger.info(f'{timezone.now()} {request.user} удалил профиль {user}')
        return Response(request.data, status.HTTP_200_OK)


class CardsListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        data = CardService.my_cards(author_id=request.user.pk)
        serializer = CardListSerializers(instance=data, many=True, context={'request': request})
        logger.info(f'{timezone.now()} {request.user} получил список карточек')
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CardCreateSerializers(data=request.data)
        if serializer.is_valid():
            CardService.create_card(author_id=request.user.pk, **serializer.data)
            logger.info(f'{timezone.now()} {request.user} добавил новую карточку')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardsDetailAPIView(APIView):
    permission_classes = [IsOwnerOrPerformersReadOnly]

    def get(self, request, *args, **kwargs):
        card = CardService.give_me_card(card_pk=kwargs['card_pk'])
        serializer = CardDetailSerializer(instance=card)
        logger.info(f'{timezone.now()} {request.user} обратился к карточке {card.pk}')
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = CardDetailUpdateSerializer(data=request.data)
        if serializer.is_valid():
            CardService.update_card(card_pk=kwargs['card_pk'], **serializer.data)
            logger.info(f'{timezone.now()} {request.user} изменил карточку')
            return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        CardService.delete_card(card_pk=kwargs['card_pk'])
        return Response({'Выполнено': "Карточка удалена"}, status.HTTP_200_OK)


class CommentListAPIView(APIView):
    permission_classes = [IsOwnerOrPerformersReadOnly]

    def get(self, request, *args, **kwargs):
        comment = CommentService().get_comments_card(
            card_pk=kwargs['card_pk']
        )
        serializer = CommentListSerializers(instance=comment, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommentCreateSerializers(data=request.data)
        if serializer.is_valid():
            CommentService().create_comment(
                author_id=request.user.pk,
                card_pk=kwargs['card_pk'],
                **serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    permission_classes = [IsOwnerOrPerformersReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            comment = CommentService().my_comment(
                card_pk=kwargs['card_pk'],
                com_pk=kwargs['com_pk'])
        except Comments.DoesNotExist:
            return Response({'Ошибка': 'Коментарий не найден'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentDetailUpdateSerializer(instance=comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = CommentDetailUpdateSerializer(data=request.data)
        if serializer.is_valid():
            CommentService().update_comment(
                card_pk=kwargs['card_pk'],
                com_pk=kwargs['com_pk'],
                **request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        CommentService().delete_comment(com_pk=kwargs['com_pk'], card_pk=kwargs['card_pk'])
        return Response({'Выполнено': "Комментарий удален"}, status=status.HTTP_200_OK)


class WorkerListAPIView(APIView):
    permission_classes = [IsOwnerOrPerformersReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            work = WorkerService().get_my_work(author_id=request.user.pk,
                                               **kwargs)
        except Worker.DoesNotExist:
            return Response({'Ошибка': 'Работа не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkerListSerializers(instance=work)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = WorkerCreateSerializers(data=request.data)
        if serializer.is_valid():
            WorkerService().create_worker(
                author_id=request.user.pk,
                card_pk=kwargs['card_pk'],
                **serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerDetailAPIView(APIView):
    permission_classes = [IsOwnerOrPerformersReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            worker = WorkerService().get_my_work(
                card_pk=kwargs['card_pk'],
                author_id=request.user.pk,
            )
        except Worker.DoesNotExist:
            return Response({'Ошибка': 'Работа не найден'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WorkerListSerializers(instance=worker)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = WorkerDetailSerializers(data=request.data)
        if serializer.is_valid():
            WorkerService().update_worker(
                card_pk=kwargs['card_pk'],
                author_id=request.user.pk,
                **request.data
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        WorkerService().delete_worker(
            card_pk=kwargs['card_pk'],
            author_id=request.user.pk
        )
        return Response({'Выполнено': "Работа удалена"}, status=status.HTTP_200_OK)


class TableListAPIView(APIView):
    """Пример POST
    {
    "planed_actors_salary": 2000.0,
    "planned_other_expenses": 2000.0,
    "planned_buying_music": 2000.0,
    "planned_travel_expenses": 2000.0,
    "planned_fare": 2000.0
    }"""
    permission_classes = [IsOwnerCard]

    def get(self, request, *args, **kwargs):
        try:
            tables = TableService().get_my_tables(**kwargs)
        except TableProject.DoesNotExist:
            return Response({'Таблиц не найдено'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TableListSerializers(instance=tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TableCreateSerializers(data=request.data)
        if serializer.is_valid():
            TableService().create_table(
                card_pk=kwargs['card_pk'],
                **serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableDetailAPIView(APIView):
    permission_classes = [IsOwnerOrPerformersReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            table = TableService().get_my_tables(card_pk=kwargs['card_pk'])
        except Worker.DoesNotExist:
            return Response({'Ошибка': 'Работа не найден'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TableListSerializers(instance=table, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('table_pk', None):
            return Response({'Ошибка': 'Таблица не найдена'}, status=status.HTTP_400_BAD_REQUEST)
        TableService().delete_table(kwargs['card_pk'], kwargs['table_pk'])
        return Response({'Выполнено': "Работа удалена"}, status=status.HTTP_200_OK)


class TableUpdatePlannedAPIView(APIView):
    permission_classes = [IsOwnerOrPerformersReadOnly]

    def put(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('table_pk', None):
            return Response({'Ошибка': 'Таблица не найдена'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TableUpdatePlannedSerializers(data=request.data)
        if serializer.is_valid():
            TableService().update_planed_table(
                card_pk=kwargs['card_pk'],
                table_pk=kwargs['table_pk'],
                **request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableUpdateFactAPIView(APIView):
    permission_classes = [IsOwnerOrPerformersReadOnly]

    def put(self, request, *args, **kwargs):
        if not kwargs.get('card_pk', None) or not kwargs.get('table_pk', None):
            return Response({'Ошибка': 'Таблица не найдена'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TableUpdateFactSerializers(data=request.data)
        if serializer.is_valid():
            TableService().update_fact_table(
                card_pk=kwargs['card_pk'],
                table_pk=kwargs['table_pk'],
                **request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableExcelAPIView(APIView):
    permission_classes = [IsOwnerCard]

    def post(self, request, *args, **kwargs):
        serializer_create = ExcelCreateSerializer(data=request.data)
        if serializer_create.is_valid():
            excel = create_excel(request.user.pk, serializer_create.data['name'], **kwargs)
            serializer = ExcelSerializer(instance=excel)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer_create.errors, status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        excel = get_my_excel_table(**kwargs)
        serializer = ExcelSerializer(instance=excel, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
