import os

from openpyxl.workbook import Workbook

from utv import settings
from utv_api.models import Worker, TableProject, Cards, Comments, TableExcel, CategoryEvent, Event
from django.core.files import File


class CardService:
    @staticmethod
    def create_card(author_id: int, title: str, description: str, deadline, performers):
        """Создает карточку проекта"""
        c = Cards.objects.create(author_id=author_id,
                                 title=title,
                                 description=description,
                                 deadline=deadline)
        for user in performers:
            c.performers.add(user)
        return c

    @staticmethod
    def my_cards(author_id: int):
        """Возвращает карточки где пользователь является автором и исполнителем"""
        return Cards.objects.filter(
            author_id=author_id).union(Cards.objects.filter(performers=author_id))

    @classmethod
    def update_card(cls, card_pk: int, title: str, description: str, deadline, performers):
        """Обновляет поля карточки"""
        c = cls.give_me_card(card_pk=card_pk)
        c.title = title
        c.description = description
        c.deadline = deadline
        for user in performers:
            c.performers.add(user)
        c.save()
        return c

    @classmethod
    def delete_card(cls, card_pk):
        """Удаляет карточку"""
        c = cls.give_me_card(card_pk=card_pk)
        c.comment.all().delete()
        c.worker.all().delete()
        c.table.all().delete()
        c.delete()

    @staticmethod
    def give_me_card(card_pk):
        """Отдаём нужную карточку по ключу"""
        card = Cards.objects.get(pk=card_pk)
        return card


class CommentService(CardService):

    def create_comment(self, author_id: int, text: str, card_pk: int, parent=None):
        """Создаёт коментарий в карточке"""
        c = Comments.objects.create(author_id=author_id, text=text, parent_id=parent)
        card = super().give_me_card(card_pk=card_pk)
        card.comment.add(c)
        return c

    def delete_comment(self, card_pk: int, com_pk: int):
        """Удаляет коментарий пользователя"""
        c = self.my_comment(card_pk=card_pk, com_pk=com_pk)
        c.delete()

    def update_comment(self, text: str, card_pk: int, com_pk: int):
        comment = self.my_comment(card_pk=card_pk, com_pk=com_pk)
        comment.text = text
        comment.save()
        return comment

    def my_comment(self, card_pk: int, com_pk: int):
        """Возвращет коментарий пользователя"""
        return super().give_me_card(card_pk=card_pk).comment.get(pk=com_pk)

    def get_comments_card(self, card_pk):
        card = super().give_me_card(card_pk=card_pk)
        return card.comment


class WorkerService(CardService):

    def create_worker(self, author_id: int, card_pk: int, actual_time: int, scheduled_time: int):
        """Создает рабочий процесс над карточкой"""
        w = Worker.objects.create(author_id=author_id,
                                  actual_time=actual_time,
                                  scheduled_time=scheduled_time)
        card = self.give_me_card(card_pk=card_pk)
        card.worker.add(w)
        return w

    def get_my_work(self, card_pk: int, author_id: int):
        """Отдает рабочий процесс пользователя созданный в карточке"""
        card = self.give_me_card(card_pk=card_pk)
        work = card.worker.get(author_id=author_id)
        return work

    def update_worker(self, **kwargs):
        """Обновляет поля рабочего процесса"""
        w = self.get_my_work(kwargs['card_pk'], kwargs['author_id'])
        w.actual_time = kwargs['actual_time']
        w.scheduled_time = kwargs['scheduled_time']
        w.save()
        return w

    def delete_worker(self, card_pk: int, author_id: int):
        """Удаляет рабочий процесс в карточке"""
        w = self.get_my_work(card_pk, author_id)
        w.delete()


class TableService(CardService):
    def executors(self, card_pk: int):
        """Собираем всех исполнителей по проекту"""
        card = self.give_me_card(card_pk=card_pk)
        return card.worker.all()

    def salary_executors(self, card_pk, planned_actors_salary: int, actors_salary: int):
        """Расчитываем заработную плату сотрудников за проект и возвращаем её в виде кортежа"""
        # Фактический заработок сотрудников за проект
        workersalary = 0
        # Плановый заработок сотрудников за проект
        planedworkersalary = 0
        for i in self.executors(card_pk=card_pk):
            for i2 in i.author.employeerate.order_by('-created_time')[:1]:
                planedworkersalary += i2.money * i.scheduled_time
                workersalary += i2.money * i.actual_time
        return planedworkersalary + planned_actors_salary, workersalary + actors_salary

    def calculation_table(self, card_pk, **kwargs):
        """Расчитываем плановые и фактические расчёты затрат и прибыли за проект"""
        # Плановая зарплата сотрудников, Зарплата сотрудников
        planned_salary, salary = self.salary_executors(
            card_pk=card_pk,
            planned_actors_salary=kwargs.get('planned_actors_salary', 0),
            actors_salary=kwargs.get('actors_salary', 0))
        # Плановые налоги с ФОТ
        planned_taxes_fot = planned_salary * 0.5
        # Налоги с ФОТ
        taxes_fot = salary * 0.5

        # Плановые общехозяйственные расходы
        list_planned_general_expenses = [
            planned_salary, planned_taxes_fot, kwargs.get('planned_other_expenses', 0),
            kwargs.get('planned_buying_music', 0), kwargs.get('planned_travel_expenses', 0),
            kwargs.get('planned_fare', 0)]
        planned_general_expenses = sum(list_planned_general_expenses) * 0.23
        # Общехозяйственные расходы
        list_general_expenses = [
            salary, taxes_fot, kwargs.get('other_expenses', 0), kwargs.get('buying_music', 0),
            kwargs.get('travel_expenses', 0), kwargs.get('fare', 0)]
        general_expenses = sum(list_general_expenses) * 0.23
        # Плановая себестоимость
        list_planned_cost = [
            planned_salary, planned_taxes_fot, kwargs.get('planned_other_expenses', 0),
            planned_general_expenses, kwargs.get('planned_buying_music', 0),
            kwargs.get('planned_travel_expenses', 0), kwargs.get('planned_fare', 0)]
        planned_cost = sum(list_planned_cost)
        # Cебестоимость
        list_cost = [salary, taxes_fot, kwargs.get('other_expenses', 0), general_expenses,
                     kwargs.get('buying_music', 0), kwargs.get('travel_expenses', 0),
                     kwargs.get('fare', 0)]
        cost = sum(list_cost)

        # Плановая прибыль
        planned_profit = kwargs.get('price_client', 15000) - planned_cost
        # Фактическая прибыль
        profit = kwargs.get('price_client', 15000) - cost
        # Плановая рентабельность
        planned_profitability = (planned_profit / kwargs.get('price_client', 15000)) * 100
        # Фактическая рентабельность
        profitability = (profit / kwargs.get('price_client', 15000)) * 100
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

    def create_table(self, card_pk: int, **kwargs):
        """Создаёт смету по созданному проекту"""
        content = self.calculation_table(card_pk=card_pk, **kwargs)
        t = TableProject.objects.create(
            price_client=15000,
            planned_actors_salary=kwargs['planned_actors_salary'],
            planned_buying_music=kwargs['planned_buying_music'],
            planned_travel_expenses=kwargs['planned_travel_expenses'],
            planned_fare=kwargs['planned_fare'],
            planned_other_expenses=kwargs['planned_other_expenses'],
            **content
        )
        card = self.give_me_card(card_pk)
        card.table.add(t)
        return t

    def get_table(self, table_pk):
        """Возвращем таблицу по ключу"""
        return TableProject.objects.get(pk=table_pk)

    def update_planed_table(self, card_pk: int, table_pk: int, **kwargs):
        """Коректируем данные таблицы в случае если
         какие то поля не заполнены либо ЗП сотрудников поменялась"""
        content = self.calculation_table(card_pk, **kwargs)
        t = self.get_table(table_pk)
        t.price_client = kwargs.get('price_client')
        t.planned_salary = content['planned_salary']
        t.planned_actors_salary = kwargs.get('planned_actors_salary')
        t.planned_taxes_FOT = content['planned_taxes_FOT']
        t.planned_general_expenses = content['planned_general_expenses']
        t.planned_cost = content['planned_cost']
        t.planned_profit = content['planned_profit']
        t.planned_profitability = content['planned_profitability']
        t.price_client = kwargs['price_client']
        t.planned_other_expenses = kwargs.get('planned_other_expenses', t.planned_other_expenses)
        t.planned_fare = kwargs.get('planned_fare', t.planned_fare)
        t.planned_travel_expenses = kwargs.get('planned_travel_expenses', t.planned_travel_expenses)
        t.planned_buying_music = kwargs.get('planned_buying_music', t.planned_buying_music)
        t.save()
        return t

    def update_fact_table(self, card_pk: int, table_pk: int, **kwargs):
        """Коректируем данные таблицы в случае если
         какие то поля не заполнены либо ЗП сотрудников поменялась"""
        content = self.calculation_table(card_pk, **kwargs)
        t = self.get_table(table_pk)
        t.price_client = kwargs.get('price_client')
        t.salary = content['salary']
        t.actors_salary = kwargs.get('actors_salary')
        t.taxes_FOT = content['taxes_FOT']
        t.general_expenses = content['general_expenses']
        t.cost = content['cost']
        t.profit = content['profit']
        t.profitability = content['profitability']
        t.price_client = kwargs['price_client']
        t.other_expenses = kwargs.get('other_expenses', t.other_expenses)
        t.fare = kwargs.get('fare', t.fare)
        t.travel_expenses = kwargs.get('travel_expenses', t.travel_expenses)
        t.buying_music = kwargs.get('buying_music', t.buying_music)
        t.save()
        return t

    def get_my_tables(self, card_pk):
        tables = self.give_me_card(card_pk=card_pk)
        return tables.table

    def delete_table(self, card_pk, table_pk):
        card = self.give_me_card(card_pk=card_pk)
        table = card.table.get(pk=table_pk)
        table.delete()


def create_excel(author_id: int, name: str, **kwargs):
    """Создаём excel файл из сформированной таблицы"""
    table = TableService().get_table(kwargs['table_pk'])
    name_file = f'{name}.xlsx'
    path = os.path.join(settings.EXCEL_ROOT, name_file)
    wb = Workbook()
    ws = wb.active
    ws['A6'] = 'ЦЕНА для клиента'
    ws['B6'] = table.price_client
    ws['A7'] = 'Плановая себестоимость'
    ws['B7'] = table.planned_cost
    ws['C7'] = 'Фактическая себестоимость'
    ws['D7'] = table.cost
    ws['A8'] = 'Плановая зарплата'
    ws['B8'] = table.planned_salary
    ws['C8'] = 'Фактическая зарплата'
    ws['D8'] = table.salary
    ws['A9'] = 'Плановый гонорар актерам'
    ws['B9'] = table.planned_actors_salary
    ws['C9'] = 'Фактический гонорар актерам'
    ws['D9'] = table.actors_salary
    ws['A10'] = 'Плановые налоги с ФОТ'
    ws['B10'] = table.planned_taxes_FOT
    ws['C10'] = 'Фактические налоги с ФОТ'
    ws['D10'] = table.taxes_FOT
    ws['A11'] = 'Плановая покупка реквизита для организации съемочного процесса/' \
                ' Непредвиденные расходы'
    ws['B11'] = table.planned_other_expenses
    ws['C11'] = 'Фактическая покупка реквизита для организации съемочного процесса/' \
                ' Непредвиденные расходы'
    ws['D11'] = table.other_expenses
    ws['A12'] = 'Плановая покупка музыки'
    ws['B12'] = table.planned_buying_music
    ws['C12'] = 'Фактическа покупка музыки'
    ws['D12'] = table.buying_music
    ws['A13'] = 'Плановые командировочные расходы (суточные, жилье, дорога)'
    ws['B13'] = table.planned_travel_expenses
    ws['C13'] = 'Фактические командировочные расходы (суточные, жилье, дорога)'
    ws['D13'] = table.travel_expenses
    ws['A14'] = 'Плановые такси, транспортные расходы '
    ws['B14'] = table.planned_fare
    ws['C14'] = 'Фактические такси, транспортные расходы '
    ws['D14'] = table.fare
    ws['A15'] = 'Плановые общехозяйственные расходы'
    ws['B15'] = table.planned_general_expenses
    ws['C15'] = 'Фактические общехозяйственные расходы'
    ws['D15'] = table.general_expenses
    ws['A16'] = 'Плановая прибыль'
    ws['B16'] = table.planned_profit
    ws['C16'] = 'Фактическая прибыль'
    ws['D16'] = table.profit
    ws['A17'] = 'Плановая рентабельность'
    ws['B17'] = table.planned_profitability
    ws['C17'] = 'Фактическая рентабельность'
    ws['D17'] = table.profitability
    wb.save(path)
    excel = TableExcel.objects.create(user_id=author_id,
                                      table_id=kwargs['table_pk'],
                                      name=name_file)
    excel.path_excel.save(name_file, File(open(path, 'rb')))
    os.remove(path)
    return excel


def get_my_excels_table(**kwargs):
    """Отдаём пользователю все excel связанные с таблицой"""
    excel = TableExcel.objects.filter(table_id=kwargs['table_pk'])
    return excel


def get_excel(excel_pk: int):
    excel = TableExcel.objects.get(pk=excel_pk)
    return excel


def delete_excel(excel_pk: int):
    excel = get_excel(excel_pk)
    excel.path_excel.delete(save=False)
    excel.delete()


def get_categorys_event():
    return CategoryEvent.objects.all()


def add_category_event(title):
    return CategoryEvent.objects.create(title=title)


def get_category_event(pk):
    return CategoryEvent.objects.get(pk=pk)


def delete_category_event(pk):
    CategoryEvent.objects.get(pk=pk).delete()


def get_events():
    return Event.objects.all()


def get_event(event_pk):
    return Event.objects.get(pk=event_pk)


def add_event(author_id: int, **kwargs):
    eve = Event.objects.create(author_id=author_id,
                               title=kwargs['title'],
                               date_begin=kwargs['date_begin'],
                               data_end=kwargs['data_end'],
                               category_id=kwargs['category'])
    for i in kwargs['performers']:
        eve.performers.add(i)
    return eve


def delete_event(event_pk):
    get_event(event_pk).delete()
