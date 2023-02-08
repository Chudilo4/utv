from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy, reverse
# Create your models here.


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/profile/avatar/', null=True,
                               default='media/profile/avatar/Default_ava.png')

    def __str__(self):
        return self.user.username


class Cards(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    performers = models.ManyToManyField(User, related_name='CardEvent', blank=True)
    date_dedlain = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('card_detail' , kwargs={'pk': self.pk})


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Поле для коментария')
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-created',)


class Worker(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    actual_time = models.IntegerField(verbose_name='Фактическое время', default=0)
    scheduled_time = models.IntegerField(verbose_name='Плановое время', default=0)

    def __str__(self):
        return self.author.username + ' ' + self.card.title


class TableProject(models.Model):
    cards = models.ForeignKey(Cards, on_delete=models.CASCADE)
    planned_cost = models.IntegerField(verbose_name='Плановая себестоимость', null=True)
    cost = models.IntegerField(verbose_name='Фактическая себестоимость', null=True)
    planned_salary = models.IntegerField(verbose_name='Плановая зарплата', null=True)
    salary = models.IntegerField(verbose_name='Фактическая зарплата', null=True)
    planned_taxes_FOT = models.IntegerField(verbose_name='Плановые налоги с ФОТ', null=True)
    taxes_FOT = models.IntegerField(verbose_name='Фактические налоги с ФОТ', null=True)
    planned_other_expenses = models.IntegerField(verbose_name='Плановые прочие расходы', null=True)
    other_expenses = models.IntegerField(verbose_name='Фактические прочие расходы', null=True)
    planned_general_expenses = models.IntegerField(verbose_name='Плановые общехозяйственные расходы', null=True)
    general_expenses = models.IntegerField(verbose_name='Фактические общехозяйственные расходы', null=True)
    planned_profit = models.IntegerField(verbose_name='Плановая прибыль', null=True)
    profit = models.IntegerField(verbose_name='Фактическая прибыль', null=True)
    planned_profitability = models.IntegerField(verbose_name='Плановая рентабельность', null=True)
    profitability = models.IntegerField(verbose_name='Фактическая рентабельность', null=True)

    def __str__(self):
        return f'Таблица {self.cards.title}'


class EmployeeRate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(verbose_name='Заработок в час', null=True)

    def __str__(self):
        return f'ЗП в час сотрудника {self.user} составляет {self.money}'


class SalaryProjectUser(models.Model):
    table_project = models.ForeignKey(TableProject, on_delete=models.CASCADE, verbose_name='Таблица проекта')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Работа сотрудника', null=True)
    planned_salary = models.IntegerField(verbose_name='Плановая зарплата', null=True)
    salary = models.IntegerField(verbose_name='Фактическая зарплата', null=True)

    def __str__(self):
        return f'Зарплата сотрудника {self.worker.author} за проект {self.table_project.cards.title}'
