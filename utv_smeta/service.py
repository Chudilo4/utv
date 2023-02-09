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
        c = Cards.objects.create(author_id=self.author_id,
                                 title=self.title,
                                 description=self.descriprion,
                                 date_dedlain=self.date_dedlain)
        for user in self.performers:
            c.performers.add(user.pk)

    def my_cards(self):
        return Cards.objects.filter(author_id=self.author_id).union(Cards.objects.filter(performers=self.author_id))

    def update_card(self):
        c = self.give_me_card()
        c.title = self.title
        c.description = self.descriprion
        c.date_dedlain = self.date_dedlain
        for user in self.performers:
            c.performers.add(user.pk)
        c.save()

    def delete_card(self):
        c = self.give_me_card()
        c.delete()

    def give_me_card(self):
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
        w = Worker.objects.create(author_id=self.author_pk,
                                  card_id=self.card_pk,
                                  actual_time=self.actual_time,
                                  scheduled_time=self.scheduled_time)

    def my_work(self):
        return Worker.objects.get(card_id=self.card_pk, author_id=self.author_pk)

    def count_worker_in_card(self):
        return Worker.objects.filter(author_id=self.author_pk, card_id=self.card_pk).count()

    def update_worker(self):
        w = self.my_work()
        w.actual_time = self.actual_time
        w.scheduled_time = self.scheduled_time
        w.save()

    def delete_worker(self):
        w = self.my_work()
        w.delete()


class CommentService:
    def __init__(self, request=None, comment_pk=None, author_pk=None, card_pk=None, text=None):
        self.author_pk = author_pk
        self.card_pk = card_pk
        self.text = text
        self.comment_pk = comment_pk
    def create_comment(self):
        c = Comments.objects.create(card_id=self.card_pk, author_id=self.author_pk, text=self.text)

    def my_comment(self):
        return Comments.objects.get(pk=self.comment_pk, card_id=self.card_pk, author_id=self.author_pk)

    def delete_comment(self):
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

    def perfomens(self):
        return Worker.objects.filter(card_id=self.card_pk)

    def create_table(self):
        planned_salary, salary = self.salary_perfomance()  # Плановая зарплата сотрудников, Зарплата сотрудников
        planned_taxes_fot = planned_salary * 0.5  # Плановые налоги с ФОТ
        taxes_fot = salary * 0.5  # Налоги с ФОТ
        planned_other_expenses = self.planned_other_expenses   #  Плановые прочие расходы
        other_expenses = self.other_expenses  # Прочие расходы
        planned_general_expenses = (planned_salary + planned_taxes_fot + planned_other_expenses) * 0.23 # Плановые общехозяйственные расходы
        general_expenses = (salary + taxes_fot + other_expenses) * 0.23  # Общехозяйственные расходы
        planned_cost = planned_salary + planned_taxes_fot + planned_other_expenses + planned_general_expenses  # Плановая себестоимость
        cost = salary + taxes_fot + other_expenses + general_expenses  # Cебестоимость
        planned_profit = self.price_client - planned_cost # Плановая прибыль
        profit = self.price_client - cost  # Фактическая прибыль
        planned_profitability = (planned_profit / self.planed_price_client) * 100  # Плановая рентабельность
        profitability = (profit / self.price_client) * 100  # Фактическая рентабельность
        TableProject.objects.create(cards_id=self.card_pk,
                                    price_client=self.price_client,
                                    planned_price_client=self.planed_price_client,
                                    planned_cost=planned_cost,
                                    cost=cost,
                                    planned_salary=planned_salary,
                                    salary=salary,
                                    planned_taxes_FOT=planned_taxes_fot,
                                    taxes_FOT=taxes_fot,
                                    planned_other_expenses=self.planned_other_expenses,
                                    other_expenses=self.other_expenses,
                                    planned_general_expenses=planned_general_expenses,
                                    general_expenses=general_expenses,
                                    planned_profit=planned_profit,
                                    profit=profit,
                                    planned_profitability=planned_profitability,
                                    profitability=profitability
                                    )

    def valid_table(self):
        return self.salary_perfomance()

    def get_table(self):
        return TableProject.objects.get(pk=self.table_pk)

    def salary_perfomance(self):
        workersalary = 0
        planedworkersalary = 0
        for i in self.perfomens():
            for i2 in i.author.employeerate_money.order_by('-creared')[:1]:
                workersalary += i2.money * i.actual_time
                planedworkersalary += i2.money * i.scheduled_time
        return planedworkersalary, workersalary
