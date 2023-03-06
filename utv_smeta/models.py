from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Cards(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    performers = models.ManyToManyField(CustomUser, related_name='CardEvent', blank=True)
    deadline = models.DateTimeField()
    comment = models.ManyToManyField('Comments', through='CommentsCards')
    table = models.ManyToManyField('TableProject', through='TableCards')
    worker = models.ManyToManyField('Worker', through='WorkerCards')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления карточки')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'card_pk': self.pk})


class Comments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    text = models.TextField(verbose_name='Поле для коментария')
    created_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created_time',)


class Worker(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    actual_time = models.IntegerField(verbose_name='Фактическое время', default=0)
    scheduled_time = models.IntegerField(verbose_name='Плановое время', default=0)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания работы')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления работы')

    def __str__(self):
        return self.author.username


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
    planed_actors_salary = models.FloatField(verbose_name='Плановая зарплата актёрам',
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

    def __str__(self):
        return f'Таблица {self.created_time}'


class EmployeeRate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employeerate')
    money = models.IntegerField(verbose_name='Заработок в час', null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'ЗП в час сотрудника {self.user} составляет {self.money}'


class TableExcel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=1)
    table = models.ForeignKey(TableProject, on_delete=models.CASCADE)
    path_excel = models.FileField(upload_to='excel/')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')


class CommentsCards(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)


class WorkerCards(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)


class TableCards(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    table = models.ForeignKey(TableProject, on_delete=models.CASCADE)
