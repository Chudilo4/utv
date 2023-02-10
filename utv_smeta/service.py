from utv_smeta.models import Worker, TableProject, Cards, EmployeeRate, SalaryProjectUser, Comments
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class CardService:
    def __init__(self, request=None, user_pk=None, title=None, description=None, performers=None,
                 date_dedlain=None, card_pk=None):
        self.author_id = user_pk
        self.title = title
        self.descriprion = description
        self.performers = performers
        self.date_dedlain = date_dedlain
        self.card_pk = card_pk
        self.request = request

    def create_card(self):
        """Создает карточку проекта"""
        c = Cards.objects.create(author_id=self.author_id,
                                 title=self.title,
                                 description=self.descriprion,
                                 date_dedlain=self.date_dedlain)
        for user in self.performers:
            c.performers.add(user.pk)

    def my_cards(self):
        """Возвращает карточки где пользователь является автором и исполнителем"""
        return Cards.objects.filter(author_id=self.author_id).union(Cards.objects.filter(performers=self.author_id))

    def update_card(self):
        """Обновляет поля карточки"""
        c = self.give_me_card()
        c.title = self.title
        c.description = self.descriprion
        c.date_dedlain = self.date_dedlain
        for user in self.performers:
            c.performers.add(user.pk)
        c.save()

    def delete_card(self):
        """Удаляет карточку"""
        c = self.give_me_card()
        c.delete()

    def give_me_card(self):
        '''Отдаём нужную карточку по ключу'''
        return Cards.objects.get(pk=self.card_pk)


class WorkerService:
    def __init__(self, request=None, work_pk=None, author_pk=None, card_pk=None, actual_time=None, scheduled_time=None):
        self.author_pk = author_pk
        self.card_pk = card_pk
        self.actual_time = actual_time
        self.scheduled_time = scheduled_time
        self.work_pk = work_pk
        self.request = request

    def create_worker(self):
        """Создает рабочий процесс над карточкой"""
        w = Worker.objects.create(author_id=self.author_pk,
                                  card_id=self.card_pk,
                                  actual_time=self.actual_time,
                                  scheduled_time=self.scheduled_time)

    def my_work(self):
        """Отдает рабочий процесс пользователя созданный в карточке"""
        return Worker.objects.get(card_id=self.card_pk, author_id=self.author_pk)

    def count_worker_in_card(self):
        """Счиатет кол-во рабочих процессов пользователя в карточке"""
        return Worker.objects.filter(author_id=self.author_pk, card_id=self.card_pk).count()

    def update_worker(self):
        """Обновляет поля рабочего процесса"""
        w = self.my_work()
        w.actual_time = self.actual_time
        w.scheduled_time = self.scheduled_time
        w.save()

    def delete_worker(self):
        """Удаляет рабочий процесс в карточке"""
        w = self.my_work()
        w.delete()


class CommentService:
    def __init__(self, request=None, comment_pk=None, author_pk=None, card_pk=None, text=None):
        self.author_pk = author_pk
        self.card_pk = card_pk
        self.text = text
        self.comment_pk = comment_pk

    def create_comment(self):
        """Создаёт коментарий в карточке"""
        c = Comments.objects.create(card_id=self.card_pk, author_id=self.author_pk, text=self.text)

    def my_comment(self):
        """Возвращет коментарий пользователя"""
        return Comments.objects.get(pk=self.comment_pk, card_id=self.card_pk, author_id=self.author_pk)

    def delete_comment(self):
        """Удаляет коментарий пользователя"""
        c = self.my_comment()
        c.delete()


class TableService:
    def __init__(self, request=None, card_pk=None, table_pk=None,
                 planned_other_expenses=1, other_expenses=1, planned_price_client=1, price_client=1):
        self.card_pk = card_pk
        self.request = request
        self.table_pk = table_pk
        self.price_client = price_client
        self.planned_other_expenses = planned_other_expenses
        self.other_expenses = other_expenses
        self.planed_price_client = planned_price_client

    def create_table(self):
        """Создаёт смету по созданному проекту"""
        t = TableProject.objects.create(cards_id=self.card_pk,
                                        planned_price_client=self.planed_price_client,
                                        planned_other_expenses=self.planned_other_expenses,
                                        )
        self.salary_perfomance(table_pk=t.pk)
        self.calculation_table(planned_price_client=self.planed_price_client,
                               planned_other_expenses=self.planned_other_expenses,
                               table_pk=t.pk)

    def performers(self):
        """Собираем всех исполнителей по проекту"""
        return Worker.objects.filter(card_id=self.card_pk)

    def valid_table(self):
        return True

    def get_table(self):
        """Возвращем таблицу по ключу"""
        return TableProject.objects.get(pk=self.table_pk)

    def salary_perfomance(self, table_pk):
        """Расчитываем заработную плату сотрудников за проект и возвращаем её в виде кортежа"""
        # Фактический заработок сотрудников за проект
        workersalary = 0
        # Плановый заработок сотрудников за проект
        planedworkersalary = 0
        for i in self.performers():
            for i2 in i.author.employeerate.order_by('-created')[:1]:
                workersalary += i2.money * i.actual_time
                planedworkersalary += i2.money * i.scheduled_time
                SalaryProjectUser.objects.create(table_project_id=table_pk,
                                                 user_id=i.author.pk,
                                                 planned_salary=planedworkersalary,
                                                 salary=workersalary)
        return planedworkersalary, workersalary

    def calculation_table(self, planned_price_client, planned_other_expenses, table_pk):
        """Расчитываем плановые и фактические расчёты затрат и прибыли за проект"""
        # Плановая зарплата сотрудников, Зарплата сотрудников
        planned_salary, salary = self.salary_perfomance(table_pk=table_pk)
        # Плановые налоги с ФОТ
        planned_taxes_fot = planned_salary * 0.5
        # Налоги с ФОТ
        taxes_fot = salary * 0.5
        # Плановые прочие расходы
        planned_other_expenses = planned_other_expenses
        # Прочие расходы
        other_expenses = self.other_expenses
        # Плановые общехозяйственные расходы
        planned_general_expenses = (planned_salary + planned_taxes_fot + planned_other_expenses) * 0.23
        # Общехозяйственные расходы
        general_expenses = (salary + taxes_fot + other_expenses) * 0.23
        # Плановая себестоимость
        planned_cost = planned_salary + planned_taxes_fot + planned_other_expenses + planned_general_expenses
        # Cебестоимость
        cost = salary + taxes_fot + other_expenses + general_expenses
        # Плановая прибыль
        planned_profit = planned_price_client - planned_cost
        # Фактическая прибыль
        profit = planned_price_client - cost
        # Плановая рентабельность
        planned_profitability = (planned_profit / planned_price_client) * 100
        # Фактическая рентабельность
        profitability = (profit / planned_price_client) * 100
        return {'planned_salary': planned_salary,
                'salary': salary,
                'planned_taxes_fot': planned_taxes_fot,
                'taxes_fot': taxes_fot,
                'planned_other_expenses': planned_other_expenses,
                'other_expenses': other_expenses,
                'planned_general_expenses': planned_general_expenses,
                'general_expenses': general_expenses,
                'planned_cost': planned_cost,
                'cost': cost,
                'planned_profit': planned_profit,
                'profit': profit,
                'planned_profitability': planned_profitability,
                'profitability': profitability,
                }

    def update_table_curent_salary(self):
        """Обновляем таблицу по имеюющейся на данный момент ставке сотрудников"""
        t = self.get_table()
        content = self.calculation_table(planned_price_client=t.planned_price_client,
                                         planned_other_expenses=t.planned_other_expenses,
                                         table_pk=t.pk)
        t.planned_cost = content['planned_cost']
        t.cost = content['cost']
        t.planned_salary = content['planned_salary']
        t.salary = content['salary']
        t.planned_taxes_FOT = content['planned_taxes_fot']
        t.taxes_FOT = content['taxes_fot']
        t.planned_other_expenses = content['planned_other_expenses']
        t.other_expenses = content['other_expenses']
        t.planned_general_expenses = content['planned_general_expenses']
        t.general_expenses = content['general_expenses']
        t.planned_profit = content['planned_profit']
        t.profit = content['profit']
        t.planned_profitability = content['planned_profitability']
        t.profitability = content['profitability']
        t.save()

    def update(self):
        """Коректируем данные таблицы в случае если какие то поля не заполнены либо ЗП сотрудников поменялась"""
        t = self.get_table()
        t.planned_price_client = self.planed_price_client
        t.price_client = self.price_client
        t.planned_other_expenses = self.planned_other_expenses
        t.other_expenses = self.other_expenses
        t.save()
        self.update_table_curent_salary()

    def actual_salary_users(self):
        # Фактический заработок сотрудников за проект
        workersalary = 0
        # Плановый заработок сотрудников за проект
        planedworkersalary = 0
        for i in SalaryProjectUser.objects.filter(table_project_id=self.table_pk):
            for i2 in i.author.employeerate.order_by('-created_time')[:1]:
                workersalary += i2.money * i.actual_time
                planedworkersalary += i2.money * i.scheduled_time
                SalaryProjectUser.objects.create(table_project_id=self.table_pk,
                                                 worker_id=i.pk,
                                                 planned_salary=planedworkersalary,
                                                 salary=workersalary)
        return planedworkersalary, workersalary




