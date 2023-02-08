from utv_smeta.models import Worker, TableProject, Cards, EmployeeRate, SalaryProjectUser
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


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





# def create_worker(request, card_pk, actual_time, scheduled_time):
#     """В этой логике при создании пользователем работы
#     происходит создание таблицы в которой указано сколько
#     пользователь получит зарплаты за своё потраченно время"""
#     c = Cards.objects.get(pk=card_pk)
#     t = TableProject.objects.get(cards=c)
#     w = Worker.objects.create(author=request.user,
#                               card=c,
#                               actual_time=actual_time,
#                               scheduled_time=scheduled_time)
#     try:
#         a_t = int(w.actual_time) * w.author.employeerate.money
#         s_t = int(w.scheduled_time) * w.author.employeerate.money
#         SalaryProjectUser.objects.create(worker=w, table_project=t, salary=a_t, planned_salary=s_t)
#     except:
#         messages.error(request, 'Вам не проставлена зарплата')
#
#
# def update_worker(worker_pk, card_pk, actual_time, scheduled_time):
#     w = Worker.objects.get(pk=worker_pk)
#     w.actual_time = actual_time
#     w.scheduled_time = scheduled_time
#     w.save()
#     c = Cards.objects.get(pk=card_pk)
#     t = TableProject.objects.get(cards=c)
#     a_t = int(w.actual_time) * w.author.employeerate.money
#     s_t = int(w.scheduled_time) * w.author.employeerate.money
#     s = SalaryProjectUser.objects.get(table_project=t, worker=w)
#     s.salary = a_t
#     s.planned_salary = s_t
#     s.save()
#
#
# def get_my_worker(card, author):
#     try:
#         w = Worker.objects.get(card=card, author=author)
#         return w
#     except:
#         return None
#
#
# def create_table(pk):
#     TableProject.objects.create(card=Cards.objects.get(pk=pk))
#
#
# def get_my_table(card):
#     t = TableProject.objects.get(cards=card)
#     t.salaryprojectuser_set
#     return t
#
#
# def get_table(table_pk):
#     return TableProject.objects.get(pk=table_pk)
#
# def refresh_table(card_id, table_pk):
#     Worker.objects.filter(card_id=card_id)
#     t = TableProject.objects.get(pk=table_pk)
#
#
# class Workers:
#     def __init__(self, card_id, author_id):
#         self.card_id = card_id
#         self.author_id = author_id
#         self.count_worker = Worker.objects.filter(card_id=self.card_id).count()
#
#     def get_my_worker(self):
#         try:
#             w = Worker.objects.get(card_id=self.card_id, author_id=self.author_id)
#             return w
#         except:
#             return None
#
#
# class TableCardsService:
#     def __init__(self, card_pk):
#         self.card_pk = card_pk
#         self.count_worker = Worker.objects.filter(card_id=self.card_pk).count()
#
#     def get_my_table(self):
#         try:
#             return TableProject.objects.get(cards_id=self.card_pk)
#         except:
#             return None
