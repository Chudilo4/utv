from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='profile/avatar/', null=True,
                               default='profile/avatar/Default_ava.png')
    telegram_id = models.CharField(null=True, verbose_name='Telegram ID', max_length=35)


class Cards(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                               null=True, verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Название проекта', blank=False)
    description = models.TextField(verbose_name='Описание проекта', blank=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    performers = models.ManyToManyField(CustomUser, related_name='CardEvent',
                                        blank=True, verbose_name='Исполнители')
    deadline = models.DateTimeField(verbose_name='Дедлайн', blank=False)
    comment = models.ManyToManyField('Comments', through='CommentsCards',
                                     verbose_name="Комментарии")
    table = models.ManyToManyField('TableProject', through='TableCards', verbose_name="Таблицы")
    worker = models.ManyToManyField('Worker', through='WorkerCards',
                                    verbose_name='Рабочее время сотрудников')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления карточки')
    archived = models.BooleanField(verbose_name='Добавить в архив', default=False, blank=True)

    def get_absolute_url(self):
        return reverse('cards_detail', kwargs={'card_pk': self.pk})

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'


class Comments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    text = models.TextField(verbose_name='Поле для коментария')
    created_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_time',)


class Worker(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    actual_time = models.IntegerField(verbose_name='Фактическое время', default=0)
    scheduled_time = models.IntegerField(verbose_name='Плановое время', default=0)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания работы')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления работы')

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'


class TableProject(models.Model):
    price_client = models.FloatField(verbose_name='Цена для клиента',
                                     null=True, blank=True)
    planned_cost = models.FloatField(verbose_name='Плановая себестоимость',
                                     null=True, blank=True)
    cost = models.FloatField(verbose_name='Фактическая себестоимость',
                             null=True, blank=True)
    planned_salary = models.FloatField(verbose_name='Плановая зарплата',
                                       null=True, blank=True)
    salary = models.FloatField(verbose_name='Фактическая зарплата',
                               null=True, blank=True)
    planned_actors_salary = models.FloatField(verbose_name='Плановая зарплата актёрам',
                                              null=True, blank=True)
    actors_salary = models.FloatField(verbose_name='Зарплата актёрам',
                                      null=True, blank=True)
    planned_taxes_FOT = models.FloatField(verbose_name='Плановые налоги с ФОТ',
                                          null=True, blank=True)
    taxes_FOT = models.FloatField(verbose_name='Фактические налоги с ФОТ',
                                  null=True, blank=True)
    planned_other_expenses = models.FloatField(
        verbose_name='Плановые Покупка реквизита для '
                     'организации съемочного процесса/ '
                     'Непредвиденные расходы', null=True, blank=True)
    other_expenses = models.FloatField(
        verbose_name='Плановые Покупка реквизита для организации '
                     'съемочного процесса/ Непредвиденные расходы',
        null=True, blank=True)
    planned_buying_music = models.FloatField(verbose_name='Плановая покупка музыки',
                                             null=True, blank=True)
    buying_music = models.FloatField(verbose_name='Фактическая покупка музыки',
                                     null=True, blank=True)
    planned_travel_expenses = models.FloatField(
        verbose_name='Плановые командировачные расходы',
        null=True, blank=True)
    travel_expenses = models.FloatField(
        verbose_name='Фактические командировачные расходы',
        null=True, blank=True)
    planned_fare = models.FloatField(verbose_name='Плановые транспортные расходы',
                                     null=True, blank=True)
    fare = models.FloatField(verbose_name='Фактические транспортные расходы',
                             null=True, blank=True)
    planned_general_expenses = models.FloatField(
        verbose_name='Плановые общехозяйственные расходы',
        null=True, blank=True)
    general_expenses = models.FloatField(
        verbose_name='Фактические общехозяйственные расходы',
        null=True, blank=True)
    planned_profit = models.FloatField(verbose_name='Плановая прибыль',
                                       null=True, blank=True)
    profit = models.FloatField(verbose_name='Фактическая прибыль',
                               null=True, blank=True)
    planned_profitability = models.FloatField(verbose_name='Плановая рентабельность',
                                              null=True, blank=True)
    profitability = models.FloatField(verbose_name='Фактическая рентабельность',
                                      null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания таблицы')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления таблицы')

    class Meta:
        verbose_name = 'Таблица'
        verbose_name_plural = 'Таблицы'


class EmployeeRate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employeerate',
                             verbose_name='Пользователь')
    money = models.IntegerField(verbose_name='Заработок в час', null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Зарплата'
        verbose_name_plural = 'Зарплаты'


class TableExcel(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=1)
    table = models.ForeignKey(TableProject, on_delete=models.CASCADE)
    path_excel = models.FileField(upload_to='excel/')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Таблица Excel'
        verbose_name_plural = 'Таблицы Excel'


class CommentsCards(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)


class WorkerCards(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)


class TableCards(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    table = models.ForeignKey(TableProject, on_delete=models.CASCADE)


class Event(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.SET_DEFAULT,
                               default=1, verbose_name='Автор')
    title = models.CharField(max_length=255,
                             blank=False,
                             verbose_name='Название события')
    date_begin = models.DateTimeField(verbose_name='Дата начала события',
                                      blank=False)
    data_end = models.DateTimeField(verbose_name='Дата конца события',
                                    blank=False)
    category = models.ForeignKey('CategoryEvent',
                                 on_delete=models.SET_DEFAULT,
                                 default=1,
                                 blank=True)
    performers = models.ManyToManyField(CustomUser,
                                        verbose_name='Исполнители',
                                        related_name='performers')
    created_time = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Событие в календаре'
        verbose_name_plural = 'События в календаре'


class CategoryEvent(models.Model):
    title = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = 'Категория события'
        verbose_name_plural = 'Категории событий'
