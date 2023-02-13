from utv_smeta.models import Worker, TableProject, Cards, EmployeeRate, Comments
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
    def __init__(self, request=None, card_pk=None, table_pk=None, planed_actors_salary=0,
                 planned_buying_music=0, planned_travel_expenses=0, travel_expenses=0, fare=0,
                 planned_other_expenses=0, other_expenses=0, price_client=15000, planned_fare=0, actors_salary=0, buying_music=0):
        self.card_pk = card_pk
        self.request = request
        self.table_pk = table_pk
        self.price_client = price_client
        self.planned_other_expenses = planned_other_expenses
        self.other_expenses = other_expenses
        self.planed_actors_salary = planed_actors_salary
        self.actors_salary = actors_salary
        self.planned_buying_music = planned_buying_music
        self.buying_music = buying_music
        self.planned_travel_expenses = planned_travel_expenses
        self.travel_expenses = travel_expenses
        self.fare = fare
        self.planned_fare = planned_fare

    def create_table(self):
        """Создаёт смету по созданному проекту"""
        content = self.calculation_table()
        TableProject.objects.create(cards_id=self.card_pk,
                                    price_client=self.price_client,
                                    planed_actors_salary=self.planed_actors_salary,
                                    planned_buying_music=self.planned_buying_music,
                                    planned_travel_expenses=self.planned_travel_expenses,
                                    planned_fare=self.planned_fare,
                                    planned_other_expenses=self.planned_other_expenses,
                                    **content
                                    )

    def performers(self):
        """Собираем всех исполнителей по проекту"""
        return Worker.objects.filter(card_id=self.card_pk)

    def valid_table(self):
        return True

    def get_table(self):
        """Возвращем таблицу по ключу"""
        return TableProject.objects.get(pk=self.table_pk)

    def salary_perfomance(self):
        """Расчитываем заработную плату сотрудников за проект и возвращаем её в виде кортежа"""
        # Фактический заработок сотрудников за проект
        workersalary = 0
        # Плановый заработок сотрудников за проект
        planedworkersalary = 0
        for i in self.performers():
            for i2 in i.author.employeerate.order_by('-created')[:1]:
                planedworkersalary += i2.money * i.scheduled_time
                workersalary += i2.money * i.actual_time
        return planedworkersalary + self.planed_actors_salary, workersalary + self.actors_salary

    def calculation_table(self,):
        """Расчитываем плановые и фактические расчёты затрат и прибыли за проект"""
        # Плановая зарплата сотрудников, Зарплата сотрудников
        planned_salary, salary = self.salary_perfomance()
        # Плановые налоги с ФОТ
        planned_taxes_fot = planned_salary * 0.5
        # Налоги с ФОТ
        taxes_fot = salary * 0.5

        # Плановые общехозяйственные расходы
        planned_general_expenses = (planned_salary + planned_taxes_fot + self.planned_other_expenses + self.planned_buying_music + self.planned_travel_expenses + self.planned_fare) * 0.23
        # Общехозяйственные расходы
        general_expenses = (salary + taxes_fot + self.other_expenses + self.buying_music + self.travel_expenses + self.fare) * 0.23
        # Плановая себестоимость
        planned_cost = planned_salary + planned_taxes_fot + self.planned_other_expenses + planned_general_expenses
        # Cебестоимость
        cost = salary + taxes_fot + self.other_expenses + general_expenses
        # Плановая прибыль
        planned_profit = self.price_client - planned_cost
        # Фактическая прибыль
        profit = self.price_client - cost
        # Плановая рентабельность
        planned_profitability = (planned_profit / self.price_client) * 100
        # Фактическая рентабельность
        profitability = (profit / self.price_client) * 100
        return {'planned_salary': planned_salary,
                'salary': salary,
                'planned_taxes_FOT': planned_taxes_fot,
                'taxes_FOT': taxes_fot,
                'planned_general_expenses': planned_general_expenses,
                'general_expenses': general_expenses,
                'planned_cost': planned_cost,
                'cost': cost,
                'planned_profit': planned_profit,
                'profit': profit,
                'planned_profitability': planned_profitability,
                'profitability': profitability
                }


    def update_planned_table(self):
        """Коректируем данные таблицы в случае если какие то поля не заполнены либо ЗП сотрудников поменялась"""
        content = self.calculation_table()
        t = self.get_table()
        t.planned_salary = content['planned_salary']
        t.planned_taxes_FOT = content['planned_taxes_FOT']
        t.planned_general_expenses = content['planned_general_expenses']
        t.planned_cost = content['planned_cost']
        t.planned_profit = content['planned_profit']
        t.planned_profitability = content['planned_profitability']
        t.price_client = self.price_client
        t.planned_other_expenses = self.planned_other_expenses
        t.planned_fare = self.planned_fare
        t.planned_travel_expenses = self.planned_travel_expenses
        t.planned_buying_music = self.planned_buying_music
        t.save()

    def update_table(self):
        """Коректируем данные таблицы в случае если какие то поля не заполнены либо ЗП сотрудников поменялась"""
        content = self.calculation_table()
        t = self.get_table()
        t.salary = content['salary']
        t.taxes_FOT = content['taxes_FOT']
        t.general_expenses = content['general_expenses']
        t.cost = content['cost']
        t.profit = content['profit']
        t.profitability = content['profitability']
        t.price_client = self.price_client
        t.other_expenses = self.other_expenses
        t.fare = self.fare
        t.travel_expenses = self.travel_expenses
        t.buying_music = self.buying_music
        t.actors_salary = self.actors_salary
        t.save()



