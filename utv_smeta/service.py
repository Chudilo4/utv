from utv_smeta.models import Worker, TableProject, Cards, Comments


class CardService:
    def __init__(self, request=None, author=None, title=None, description=None, performers=None,
                 deadline=None, card_pk=None, text=None, comment_pk=None, parent=None,
                 planed_actors_salary=0, table_pk=None, work_pk=None,
                 planned_buying_music=0, planned_travel_expenses=0, travel_expenses=0, fare=0,
                 planned_other_expenses=0, other_expenses=0, price_client=15000, planned_fare=0, actors_salary=0,
                 buying_music=0, actual_time=0, scheduled_time=0):
        self.author_id = author
        self.title = title
        self.descriprion = description
        self.performers = performers
        self.deadline = deadline
        self.card_pk = card_pk
        self.request = request
        self.text = text
        self.comment_pk = comment_pk
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
        self.table_pk = table_pk
        self.actual_time = actual_time
        self.scheduled_time = scheduled_time
        self.work_pk = work_pk
        self.parent = parent

    def create_card(self):
        """Создает карточку проекта"""
        c = Cards.objects.create(author_id=self.author_id,
                                 title=self.title,
                                 description=self.descriprion,
                                 deadline=self.deadline)
        for user in self.performers:
            c.performers.add(user)

    def my_cards(self):
        """Возвращает карточки где пользователь является автором и исполнителем"""
        return Cards.objects.filter(author_id=self.author_id).union(Cards.objects.filter(performers=self.author_id))

    def update_card(self):
        """Обновляет поля карточки"""
        c = self.give_me_card()
        c.title = self.title
        c.description = self.descriprion
        c.deadline = self.deadline
        for user in self.performers:
            c.performers.add(user)
        c.save()
        return c

    def delete_card(self):
        """Удаляет карточку"""
        c = self.give_me_card()
        c.comment.all().delete()
        c.worker.all().delete()
        c.table.all().delete()
        c.delete()

    def give_me_card(self):
        '''Отдаём нужную карточку по ключу'''
        return Cards.objects.get(pk=self.card_pk)

    def create_comment(self):
        """Создаёт коментарий в карточке"""
        c = Comments.objects.create(author_id=self.author_id, text=self.text, parent_id=self.parent)
        card = self.give_me_card()
        card.comment.add(c)
        return card

    def delete_comment(self):
        """Удаляет коментарий пользователя"""
        c = self.my_comment()
        c.delete()

    def my_comment(self):
        """Возвращет коментарий пользователя"""
        return Comments.objects.get(pk=self.comment_pk, author_id=self.author_id)

    def get_my_comments(self):
        card = self.give_me_card()
        return card.comment

    def create_worker(self):
        """Создает рабочий процесс над карточкой"""
        w = Worker.objects.create(author_id=self.author_id,
                                  actual_time=self.actual_time,
                                  scheduled_time=self.scheduled_time)
        card = self.give_me_card()
        card.worker.add(w)

    def get_my_work(self):
        """Отдает рабочий процесс пользователя созданный в карточке"""
        card = self.give_me_card()
        return card.worker.get(author_id=self.author_id)

    def update_worker(self):
        """Обновляет поля рабочего процесса"""
        w = self.get_my_work()
        w.actual_time = self.actual_time
        w.scheduled_time = self.scheduled_time
        w.save()

    def delete_worker(self):
        """Удаляет рабочий процесс в карточке"""
        w = self.get_my_work()
        w.delete()

    def executors(self):
        """Собираем всех исполнителей по проекту"""
        card = self.give_me_card()
        return card.worker.all()

    def salary_executors(self):
        """Расчитываем заработную плату сотрудников за проект и возвращаем её в виде кортежа"""
        # Фактический заработок сотрудников за проект
        workersalary = 0
        # Плановый заработок сотрудников за проект
        planedworkersalary = 0
        for i in self.executors():
            for i2 in i.author.employeerate.order_by('-created_time')[:1]:
                planedworkersalary += i2.money * i.scheduled_time
                workersalary += i2.money * i.actual_time
        return planedworkersalary + self.planed_actors_salary, workersalary + self.actors_salary

    def calculation_table(self):
        """Расчитываем плановые и фактические расчёты затрат и прибыли за проект"""
        # Плановая зарплата сотрудников, Зарплата сотрудников
        planned_salary, salary = self.salary_executors()
        # Плановые налоги с ФОТ
        planned_taxes_fot = planned_salary * 0.5
        # Налоги с ФОТ
        taxes_fot = salary * 0.5

        # Плановые общехозяйственные расходы
        planned_general_expenses = (planned_salary + planned_taxes_fot + self.planned_other_expenses +
                                    self.planned_buying_music + self.planned_travel_expenses + self.planned_fare) * 0.23
        # Общехозяйственные расходы
        general_expenses = (salary + taxes_fot + self.other_expenses +
                            self.buying_music + self.travel_expenses + self.fare) * 0.23
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

    def create_table(self):
        """Создаёт смету по созданному проекту"""
        content = self.calculation_table()
        t = TableProject.objects.create(
                                        price_client=self.price_client,
                                        planed_actors_salary=self.planed_actors_salary,
                                        planned_buying_music=self.planned_buying_music,
                                        planned_travel_expenses=self.planned_travel_expenses,
                                        planned_fare=self.planned_fare,
                                        planned_other_expenses=self.planned_other_expenses,
                                        **content
                                        )
        card = self.give_me_card()
        card.table.add(t)
        return t



    def get_table(self):
        """Возвращем таблицу по ключу"""
        return TableProject.objects.get(pk=self.table_pk)



    def update_planned_table(self):
        """Коректируем данные таблицы в случае если
         какие то поля не заполнены либо ЗП сотрудников поменялась"""
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
        """Коректируем данные таблицы в случае если какие то
         поля не заполнены либо ЗП сотрудников поменялась"""
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

    def get_my_tables(self):
        tables = self.give_me_card()
        return tables.table

    def delete_table(self):
        card = self.give_me_card()
        table = card.table.get(pk=self.table_pk)
        table.delete()



