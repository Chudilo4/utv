from utv_smeta.models import Worker, TableProject, Cards, EmployeeRate, SalaryProjectUser
from django.contrib import messages


def create_worker(request, card_pk, actual_time, scheduled_time):
    """В этой логике при создании пользователем работы
    происходит создание таблицы в которой указано сколько
    пользователь получит зарплаты за своё потраченно время"""
    c = Cards.objects.get(pk=card_pk)
    t = TableProject.objects.get(cards=c)
    w = Worker.objects.create(author=request.user,
                              card=c,
                              actual_time=actual_time,
                              scheduled_time=scheduled_time)
    try:
        a_t = int(w.actual_time) * w.author.employeerate.money
        s_t = int(w.scheduled_time) * w.author.employeerate.money
        SalaryProjectUser.objects.create(worker=w, table_project=t, salary=a_t, planned_salary=s_t)
    except:
        messages.error(request, 'Вам не проставлена зарплата')


def update_worker(worker_pk, card_pk, actual_time, scheduled_time):
    w = Worker.objects.get(pk=worker_pk)
    w.actual_time = actual_time
    w.scheduled_time = scheduled_time
    w.save()
    c = Cards.objects.get(pk=card_pk)
    t = TableProject.objects.get(cards=c)
    a_t = int(w.actual_time) * w.author.employeerate.money
    s_t = int(w.scheduled_time) * w.author.employeerate.money
    s = SalaryProjectUser.objects.get(table_project=t, worker=w)
    s.salary = a_t
    s.planned_salary = s_t
    s.save()


def get_my_worker(card, author):
    try:
        w = Worker.objects.get(card=card, author=author)
        return w
    except:
        return None


def create_table(pk):
    TableProject.objects.create(card=Cards.objects.get(pk=pk))


def get_my_table(card):
    t = TableProject.objects.get(cards=card)
    t.salaryprojectuser_set
    return t


def get_table(table_pk):
    return TableProject.objects.get(pk=table_pk)

def refresh_table(card_id, table_pk):
    Worker.objects.filter(card_id=card_id)
    t = TableProject.objects.get(pk=table_pk)


class Workers():
    def __init__(self, card_id, author_id):
        self.card_id = card_id
        self.author_id = author_id
        self.count_worker = Worker.objects.filter(card_id=self.card_id).count()

    def get_my_worker(self):
        try:
            w = Worker.objects.get(card_id=self.card_id, author_id=self.author_id)
            return w
        except:
            return None
