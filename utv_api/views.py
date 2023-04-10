import logging

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service_app.service import (
    create_excel,
    calculation_table)
from utv_api.models import Comments, Worker, TableProject, Cards
from utv_api.models import CustomUser, TableExcel
from utv_api.permissions import (
    IsUser,
    IsOwnerCardOrReadPerformers,
    IsAuthor,
    OnlyAuthorCard,
    OnlyPerformers
)
from utv_api.serializers import (
    UserReadSerializer,
    UserCreateSerializers,
    UserDetailSerializers,
    CardListSerializers,
    CardDetailSerializer,
    CardCreateSerializers,
    CardDetailUpdateSerializer,
    CommentCreateUpdateSerializers,
    CommentListSerializers,
    WorkerListSerializers,
    WorkerCreateUpdateSerializers,
    TableListSerializers,
    TableCreateSerializers,
    TableUpdatePlannedSerializers,
    TableUpdateFactSerializers,
    ExcelSerializer,
    ExcelCreateSerializer,
)

logger = logging.getLogger(__name__)


class UsersReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = UserReadSerializer(users, many=True, context={'request': request})
        logger.info(f'{timezone.datetime.now()} {request.user} получил список пользователей')
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
            logger.info(f'{timezone.datetime.now()} Зарегестрировался новый пользователь')
            return Response(serializer2.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [IsUser]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs['user_pk'])
        serializer = UserReadSerializer(user, context={'request': request})
        logger.info(f'{timezone.datetime.now()} {request.user} обратился к своему профилю')
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs['user_pk'])
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
            logger.info(f'{timezone.datetime.now()} {request.user} поменял свой профиль')
            serializer2 = UserReadSerializer(instance=user)
            return Response(serializer2.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs['user_pk'])
        user.delete()
        logger.info(f'{timezone.datetime.now()} {request.user} удалил профиль {user}')
        return Response(request.data, status.HTTP_200_OK)


class CardsListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Пользователь получил карточку"""
        cards = Cards.objects.select_related('author').prefetch_related('performers').filter(
            author_id=request.user.pk).union(
            Cards.objects.select_related('author').prefetch_related('performers').filter(
                performers=request.user.pk))
        serializer = CardListSerializers(instance=cards, many=True, context={'request': request})
        logger.info(f'{timezone.datetime.now()} {request.user} получил список карточек')
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Пользователь создаёт карточку"""
        serializer = CardCreateSerializers(data=request.data, context={"request": request})
        if serializer.is_valid():
            card = Cards.objects.create(
                author_id=request.user.pk,
                title=serializer.data['title'],
                description=serializer.data['description'],
                deadline=serializer.data['deadline'])
            for user in serializer.data['performers']:
                card.performers.add(user)
            logger.info(f'{timezone.datetime.now()} {request.user} добавил новую карточку')
            serializer2 = CardDetailSerializer(instance=card, context={'request': request})
            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardsDetailAPIView(APIView):
    permission_classes = [IsOwnerCardOrReadPerformers]

    def get(self, request, *args, **kwargs):
        """Пользователь обратился к карточке"""
        card = get_object_or_404(
            Cards.objects.select_related('author').prefetch_related(
                'performers', 'comments_card', 'comments_card__author', 'workers_card',

            ),
            pk=kwargs['card_pk']
        )
        self.check_object_permissions(request, card)
        serializer = CardDetailSerializer(instance=card, context={"request": request})
        logger.info(f'{timezone.datetime.now()} {request.user} обратился к карточке {card.pk}')
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """Пользователь меняет карточку"""
        card = get_object_or_404(Cards, pk=kwargs['card_pk'])
        self.check_object_permissions(request, card)
        serializer = CardDetailUpdateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            card.title = serializer.data.get('title', card.title)
            card.description = serializer.data.get('description', card.description)
            card.deadline = serializer.data.get('deadline', card.deadline)
            for user in serializer.data.get('performers', card.performers.all()):
                card.performers.add(user)
            card.save()
            logger.info(f'{timezone.datetime.now()} {request.user} изменил карточку')
            serializer2 = CardDetailSerializer(instance=card, context={"request": request})
            return Response(serializer2.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """Пользователь удаляет карточку"""
        card = get_object_or_404(Cards, pk=kwargs['card_pk'])
        self.check_object_permissions(request, card)
        card.delete()
        return Response({'Выполнено': "Карточка удалена"}, status.HTTP_200_OK)


class CommentListAPIView(APIView):
    permission_classes = [OnlyPerformers]

    def get(self, request, *args, **kwargs):
        """Получаем все коментарии к карточке"""
        comment = Comments.objects.filter(card_id=kwargs['card_pk'])
        self.check_object_permissions(request, comment)
        serializer = CommentListSerializers(instance=comment, many=True,
                                            context={"request": request})
        logger.info(f'{request.user} получил список комментариев')
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Оставляем коментарий к карточке"""
        serializer = CommentCreateUpdateSerializers(
            data=request.data,
            context={"request": request})
        if serializer.is_valid():
            comment = Comments.objects.create(
                author_id=request.user.pk,
                text=serializer.data['text'],
                card_id=kwargs['card_pk']
            )
            serializer2 = CommentListSerializers(
                instance=comment,
                context={"request": request})
            logger.info(f'{request.user} оставил комментарий {comment.pk}')
            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthor]

    def get(self, request, *args, **kwargs):
        """Получить конкретный коментарий"""
        comment = get_object_or_404(Comments.objects.select_related('author'), pk=kwargs['com_pk'])
        self.check_object_permissions(request, comment)
        serializer = CommentListSerializers(instance=comment, context={"request": request})
        logger.info(f'{request.user} получил комментарий {comment.pk}')
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """Изменить коомментарий"""
        comment = get_object_or_404(Comments, pk=kwargs['com_pk'])
        self.check_object_permissions(request, comment)
        serializer = CommentCreateUpdateSerializers(data=request.data, context={"request": request})
        if serializer.is_valid():
            comment.text = serializer.data.get('text', comment.text)
            comment.save()
            logger.info(f'{request.user} изменил комментарий {comment.pk}')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """Удалить комментарий"""
        comment = get_object_or_404(Comments, pk=kwargs['com_pk'])
        self.check_object_permissions(request, comment)
        comment.delete()
        logger.info(f'{request.user} удалил комментарий')
        return Response({'Выполнено': "Комментарий удален"}, status=status.HTTP_200_OK)


class WorkerListAPIView(APIView):
    permission_classes = [OnlyPerformers]

    def get(self, request, *args, **kwargs):
        """Получить рабочее время над проектом"""
        work = Worker.objects.filter(card_id=kwargs['card_pk'])
        serializer = WorkerListSerializers(instance=work,
                                           context={"request": request},
                                           many=True)
        logger.info(f'{request.user} получил список работ {work}')
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Создать рабочее время над проектом"""
        if Worker.objects.filter(card_id=kwargs['card_pk'], author=request.user).count() > 0:
            return Response({'Предупреждение': 'Нельзя создавать больше одной работы над проектом'})
        serializer = WorkerCreateUpdateSerializers(data=request.data)
        if serializer.is_valid():
            work = Worker.objects.create(
                author_id=request.user.pk,
                actual_time=serializer.data['actual_time'],
                scheduled_time=serializer.data['scheduled_time'],
                card_id=kwargs['card_pk'])
            serializer2 = WorkerListSerializers(instance=work, context={"request": request})
            logger.info(f'{request.user} создал работу {work.pk}')
            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerDetailAPIView(APIView):
    permission_classes = [IsAuthor]

    def get(self, request, *args, **kwargs):
        """Получить созданное время над проектом"""
        work = get_object_or_404(Worker.objects.select_related('author'), pk=kwargs['work_pk'])
        self.check_object_permissions(request, work)
        serializer = WorkerListSerializers(instance=work, context={"request": request})
        logger.info(f'{request.user} получил работу {work.pk}')
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """Изменить созданное время над проектом"""
        work = get_object_or_404(Worker.objects, pk=kwargs['work_pk'])
        self.check_object_permissions(request, work)
        serializer = WorkerCreateUpdateSerializers(data=request.data)
        if serializer.is_valid():
            work.actual_time = serializer.data.get('actual_time', work.actual_time)
            work.scheduled_time = serializer.data.get('scheduled_time', work.scheduled_time)
            work.save()
            serializer2 = WorkerListSerializers(instance=work, context={"request": request})
            logger.info(f'{request.user} изменил работу {work.pk}')
            return Response(serializer2.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """Удалить созданное время над проектом"""
        work = get_object_or_404(Worker, pk=kwargs['work_pk'])
        self.check_object_permissions(request, work)
        work.delete()
        logger.info(f'{request.user} удалил работу {work.pk}')
        return Response({'Выполнено': "Работа удалена"}, status=status.HTTP_200_OK)


class TableListAPIView(APIView):
    permission_classes = [OnlyAuthorCard]

    def get(self, request, *args, **kwargs):
        """Получить список таблиц"""
        tables = TableProject.objects.select_related('author').filter(card_id=kwargs['card_pk'])
        serializer = TableListSerializers(instance=tables, many=True)
        logger.info(f'{request.user} получил список таблиц ')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Создать таблицу"""
        serializer = TableCreateSerializers(data=request.data)
        if serializer.is_valid():
            content = calculation_table(card_pk=kwargs['card_pk'], **serializer.data)
            t = TableProject.objects.create(
                price_client=15000,
                card_id=kwargs['card_pk'],
                planned_actors_salary=serializer.data['planned_actors_salary'],
                planned_buying_music=serializer.data['planned_buying_music'],
                planned_travel_expenses=serializer.data['planned_travel_expenses'],
                planned_fare=serializer.data['planned_fare'],
                planned_other_expenses=serializer.data['planned_other_expenses'],
                **content
            )
            serializer2 = TableListSerializers(instance=t)
            logger.info(f'{request.user} создал таблицу {t.pk}')
            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableDetailAPIView(APIView):
    permission_classes = [OnlyAuthorCard]

    def get(self, request, *args, **kwargs):
        """Получить таблицу"""
        table = get_object_or_404(
            TableProject.objects.select_related('author'),
            pk=kwargs['table_pk'])
        serializer = TableListSerializers(instance=table, context={'request': request})
        logger.info(f'{request.user} таблицу {table.pk}')
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Удалить таблицу"""
        table = get_object_or_404(TableProject, pk=kwargs['table_pk'])
        self.check_object_permissions(request, table)
        table.delete()
        logger.info(f'{request.user} удалил таблицу {table.pk}')
        return Response({'Выполнено': "Таблица удалена"}, status=status.HTTP_200_OK)


class TableUpdatePlannedAPIView(APIView):
    permission_classes = [IsAuthor]

    def put(self, request, *args, **kwargs):
        """Изменить плановые значения в таблице и ценник для клиента"""
        table = get_object_or_404(TableProject, pk=kwargs['table_pk'])
        serializer = TableUpdatePlannedSerializers(data=request.data)
        if serializer.is_valid():
            content = calculation_table(card_pk=kwargs['card_pk'], **serializer.data)
            table.price_client = serializer.data.get('price_client', table.price_client)
            table.planned_salary = content['planned_salary']
            table.planned_actors_salary = serializer.data.get(
                'planned_actors_salary', table.planned_actors_salary)
            table.planned_taxes_FOT = content['planned_taxes_FOT']
            table.planned_general_expenses = content['planned_general_expenses']
            table.planned_cost = content['planned_cost']
            table.planned_profit = content['planned_profit']
            table.planned_profitability = content['planned_profitability']
            table.price_client = serializer.data['price_client']
            table.planned_other_expenses = serializer.data.get(
                'planned_other_expenses', table.planned_other_expenses)
            table.planned_fare = serializer.data.get('planned_fare', table.planned_fare)
            table.planned_travel_expenses = serializer.data.get(
                'planned_travel_expenses', table.planned_travel_expenses)
            table.planned_buying_music = serializer.data.get(
                'planned_buying_music', table.planned_buying_music)
            table.save()
            serializer2 = TableListSerializers(instance=table, context={'request': request})
            logger.info(f'{request.user} изменил фактические значения в таблице {table.pk}')
            return Response(serializer2.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableUpdateFactAPIView(APIView):
    permission_classes = [IsAuthor]

    def put(self, request, *args, **kwargs):
        """Изменить фактические значения в таблице и ценник для клиента"""
        table = get_object_or_404(TableProject, pk=kwargs['table_pk'])
        serializer = TableUpdateFactSerializers(data=request.data)
        if serializer.is_valid():
            content = calculation_table(card_pk=kwargs['card_pk'], **serializer.data)
            table.price_client = serializer.data.get('price_client')
            table.salary = content['salary']
            table.actors_salary = serializer.data.get('actors_salary')
            table.taxes_FOT = content['taxes_FOT']
            table.general_expenses = content['general_expenses']
            table.cost = content['cost']
            table.profit = content['profit']
            table.profitability = content['profitability']
            table.price_client = serializer.data['price_client']
            table.other_expenses = serializer.data.get('other_expenses', table.other_expenses)
            table.fare = serializer.data.get('fare', table.fare)
            table.travel_expenses = serializer.data.get('travel_expenses', table.travel_expenses)
            table.buying_music = serializer.data.get('buying_music', table.buying_music)
            table.save()
            serializer2 = TableListSerializers(instance=table, context={'request': request})
            logger.info(f'{request.user} изменил фактические значения в таблице {table.pk}')
            return Response(serializer2.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExcelAPIView(APIView):
    permission_classes = [OnlyAuthorCard]

    def get(self, request, *args, **kwargs):
        """Получить список Excel файлов"""
        excel = TableExcel.objects.filter(table_id=kwargs['table_pk'])
        serializer = ExcelSerializer(instance=excel, many=True, context={'request': request})
        logger.info(f'{timezone.datetime.now()} {request.user} смотрит excel файлы')
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Создать Excel файл"""
        serializer_create = ExcelCreateSerializer(data=request.data)
        if serializer_create.is_valid():
            excel = create_excel(author_id=request.user.pk,
                                 name=serializer_create.data['name'], **kwargs)
            serializer = ExcelSerializer(instance=excel, context={'request': request})
            logger.info(f'{timezone.datetime.now()} {request.user} создал excel')
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer_create.errors, status.HTTP_400_BAD_REQUEST)


class ExcelDetailAPIView(APIView):
    permission_classes = [IsAuthor]

    def get(self, request, *args, **kwargs):
        """Получил Excel файл"""
        excel = get_object_or_404(TableExcel, pk=kwargs['excel_pk'])
        serializer = ExcelSerializer(instance=excel, context={'request': request})
        logger.info(f'{timezone.datetime.now()} {request.user} смотрит excel')
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Удалил Excel файл"""
        excel = get_object_or_404(TableExcel, pk=kwargs['excel_pk'])
        self.check_object_permissions(request, excel)
        excel.delete()
        logger.info(f'{timezone.datetime.now()} {request.user} удалил excel')
        return Response({'Excel': 'Успешно удалён'}, status.HTTP_200_OK)
