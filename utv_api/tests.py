from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser
from utv_smeta.models import Cards, EmployeeRate


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('users_register')
        url_users = reverse('users_list')
        data = {'username': 'Nikita',
                'password': '123456789Zz',
                'first_name': 'Artem',
                'last_name': 'Bochkarev',
                }
        response = self.client.get(url_users)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(CustomUser.objects.count(), 0)
        response_post = self.client.post(url, data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.get(username='Nikita').username, 'Nikita')
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_read_user(self):
        url = reverse('users_register')
        url_users = reverse('users_list')
        data = {'username': 'Nikita',
                'password': '123456789Zz',
                'first_name': 'Nikita',
                'last_name': 'Metelev',
                }
        data2 = {'username': 'Artem',
                 'password': '123456789Zz',
                 'first_name': 'Artem',
                 'last_name': 'Bochkarev',
                 }
        self.client.post(url, data)
        self.client.post(url, data2)
        self.client.login(username="Nikita", password='123456789Zz')
        response = self.client.get(url_users)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, [
            {"id": 1,
             "username": "Nikita",
             "avatar": "/media/media/profile/avatar/Default_ava.png",
             "first_name": "Nikita",
             "last_name": "Metelev"
             },
            {
                "id": 2,
                "username": "Artem",
                "avatar": "/media/media/profile/avatar/Default_ava.png",
                "first_name": "Artem",
                "last_name": "Bochkarev"
            }])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        """Тест на изменения аккаунта пользователя"""
        url = reverse('users_register')
        data = {'username': 'Nikita',
                'password': '123456789Zz',
                'first_name': 'Nikita',
                'last_name': 'Metelev',
                }
        self.client.post(url, data)
        url_put = reverse('users_detail', kwargs={'user_pk': 1})
        data_put = {'username': 'Artem',
                    'password': '987654321zZ',
                    'first_name': 'Artem',
                    'last_name': 'Bochkarev',
                    }
        self.client.login(username='Nikita', password='123456789Zz')
        response = self.client.put(url_put, data_put)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.get(pk=1).username, "Artem")

    def test_delete_user(self):
        url = reverse('users_register')
        url_delete = reverse('users_detail', kwargs={'user_pk': 2})
        data = {'username': 'Nikita',
                'password': '123456789Zz',
                'first_name': 'Nikita',
                'last_name': 'Metelev',
                }
        data2 = {'username': 'Artem',
                 'password': '123456789Zz',
                 'first_name': 'Artem',
                 'last_name': 'Bochkarev',
                 }
        self.client.post(url, data)
        self.client.post(url, data2)
        self.assertEqual(CustomUser.objects.all().count(), 2)
        self.client.login(username='Nikita', password='123456789Zz')
        response = self.client.delete(url_delete)
        self.assertEqual(CustomUser.objects.all().count(), 1)
        self.assertEqual(response.status_code, 200)


class CardTests(APITestCase):
    def test_create_card(self):
        url = reverse('cards_list')
        data = {
            "title": "Тестовая карточка",
            "description": "Описание для тестовой карточки",
            'performers': [1],
            "deadline": "2023-02-28T12:00:00+05:00",
        }
        CustomUser.objects.create_user('Artem', password='123456789Zz')
        self.client.login(username='Artem', password='123456789Zz')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cards.objects.count(), 0)
        response2 = self.client.post(url, data)
        self.assertEqual(Cards.objects.count(), 1)
        self.assertEqual(Cards.objects.get(title="Тестовая карточка").title, 'Тестовая карточка')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_delete_card(self):
        user = CustomUser.objects.create_user('Artem', password='123456789Zz')
        data = {
            "title": "Тестовая карточка",
            "description": "Описание для тестовой карточки",
            "deadline": "2023-02-28T12:00:00+05:00",
        }
        card = Cards.objects.create(author=user, **data)
        self.client.login(username='Artem', password='123456789Zz')
        url = reverse('cards_detail', kwargs={'card_pk': card.pk})
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), 11)
        response_delete = self.client.delete(url)
        self.assertEqual(Cards.objects.count(), 0)
        self.assertEqual(response_delete.status_code, 200)

    def test_update_card(self):
        user = CustomUser.objects.create_user('Artem', password='123456789Zz')
        CustomUser.objects.create_user('Nikita', password='123456789Zz')
        data = {
            "title": "Тестовая карточка",
            "description": "Описание для тестовой карточки",
            "deadline": "2023-02-28T12:00:00+05:00",
        }
        data2 = {
            "title": "Тестовая карточкацуцацац",
            "description": "Описание для тестовой карточкиqwe",
            "deadline": '2023-02-28T12:00:00+05:00',
            'performers': [1, 2]
        }
        card = Cards.objects.create(author=user, **data)
        self.client.login(username='Artem', password='123456789Zz')
        url = reverse('cards_detail', kwargs={'card_pk': card.pk})
        response = self.client.put(url, data2, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_read_card(self):
        user = CustomUser.objects.create_user('Artem', password='123456789Zz')
        card = Cards.objects.create(author=user,
                                    title="Тестовая карточкацуцацац",
                                    description="Описание для тестовой карточкиqwe",
                                    deadline="2023-02-28T12:00:00+05:00",
                                    )
        card.performers.add(user)
        self.client.login(username='Artem', password='123456789Zz')
        url = reverse('cards_list')
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), 1)


class CommentTests(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create_user('Artem', password='123456789Zz')
        self.card = Cards.objects.create(author=user,
                                         title="Тестовая карточкацуцацац",
                                         description="Описание для тестовой карточкиqwe",
                                         deadline="2023-02-28T12:00:00+05:00",
                                         )
        self.card.performers.add(user)
        self.client.login(username='Artem', password='123456789Zz')
        self.url = reverse('comment_list', kwargs={'card_pk': self.card.pk})

    def test_create_comment(self):
        response = self.client.post(self.url, {"text": "Тест коментария"})
        self.assertEqual(self.card.comment.get(text="Тест коментария").text, "Тест коментария")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)

    def test_delete_comment(self):
        self.client.post(self.url, {"text": "Тест коментария"})
        self.assertEqual(self.card.comment.count(), 1)
        com_pk = self.card.comment.get(text="Тест коментария").pk
        response = self.client.delete(
            path=reverse('comment_detail', kwargs={'card_pk': self.card.pk,
                                                   'com_pk': com_pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.card.comment.count(), 0)


class WorkerTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('Artem', password='123456789Zz')
        self.card = Cards.objects.create(author=self.user,
                                         title="Тестовая карточкацуцацац",
                                         description="Описание для тестовой карточкиqwe",
                                         deadline="2023-02-28T12:00:00+05:00",
                                         )
        self.card.performers.add(self.user)
        self.client.login(username='Artem', password='123456789Zz')
        self.url = reverse('worker_create', kwargs={'card_pk': self.card.pk})

    def test_create_worker(self):
        response = self.client.post(self.url, {"actual_time": 5,
                                               "scheduled_time": 4})
        self.assertEqual(self.card.worker.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(self.card.worker.get(author=self.user).actual_time, 5)
        self.assertEqual(self.card.worker.get(author=self.user).scheduled_time, 4)

    def test_update_worker(self):
        self.client.post(self.url, {"actual_time": 5,
                                    "scheduled_time": 4})
        w = self.card.worker.get(author=self.user)
        url = reverse('worker_detail', kwargs={'card_pk': self.card.pk,
                                               'work_pk': w.pk})
        response = self.client.put(url,
                                   '{"actual_time": 3, "scheduled_time": 3}',
                                   content_type='application/json')
        self.assertEqual(self.card.worker.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(self.card.worker.get(author=self.user).actual_time, 3)
        self.assertEqual(self.card.worker.get(author=self.user).scheduled_time, 3)

    def test_delete_work(self):
        self.client.post(self.url, {"actual_time": 5,
                                    "scheduled_time": 4})
        w = self.card.worker.get(author=self.user)
        url = reverse('worker_detail', kwargs={'card_pk': self.card.pk,
                                               'work_pk': w.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.card.worker.count(), 0)


class TableTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('Artem', password='123456789Zz')
        EmployeeRate.objects.create(user=self.user, money=200)
        data = {
            "title": "Тестовая карточка",
            "description": "Описание для тестовой карточки",
            'performers': [1],
            "deadline": "2023-02-28T12:00:00+05:00",
        }
        self.client.login(username='Artem', password='123456789Zz')
        self.url_card = reverse('cards_list')
        self.client.post(self.url_card, data)
        self.card = Cards.objects.get(title="Тестовая карточка")
        self.url_worker = reverse('worker_create', kwargs={'card_pk': self.card.pk})
        self.url_comment = reverse('comment_list', kwargs={'card_pk': self.card.pk})
        self.url_table = reverse('table_list', kwargs={"card_pk": self.card.pk})
        self.client.post(self.url_comment, {"text": "Тест коментария"})
        self.client.post(self.url_worker, {"actual_time": 5, "scheduled_time": 4})

    def test_created_table(self):
        response = self.client.post(self.url_table, {"planed_actors_salary": 2000,
                                                     "planned_other_expenses": 2000,
                                                     "planned_buying_music": 2000,
                                                     "planned_travel_expenses": 2000,
                                                     "planned_fare": 2000})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.card.table.count(), 1)
        # table = self.card.table.get(planned_other_expenses=2000.0)
        # self.assertEqual(table.planned_salary, 2800)
        # self.assertEqual(table.planned_cost, 15006)
        # self.assertEqual(table.planned_taxes_FOT, 1400)
        # self.assertEqual(table.planned_general_expenses, 2806)
        # self.assertEqual(table.planned_profit, -6)

    def test_update_planned_table(self):
        self.client.post(self.url_table, {"planed_actors_salary": 2000,
                                          "planned_other_expenses": 2000,
                                          "planned_buying_music": 2000,
                                          "planned_travel_expenses": 2000,
                                          "planned_fare": 2000})
        table = self.card.table.get(planed_actors_salary=2000)
        url_table_detail = reverse('table_planned_detail',
                                   kwargs={'card_pk': self.card.pk,
                                           'table_pk': table.pk})
        response = self.client.put(url_table_detail,
                                   '''{"planed_actors_salary": 2000,
                                   "planned_other_expenses": 2000,
                                   "planned_buying_music": 2000,
                                   "planned_travel_expenses": 2000,
                                   "planned_fare": 2000,
                                   "price_client": 150000}''',
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.card.table.count(), 1)
        table = self.card.table.get(price_client=150000)
        self.assertEqual(table.planned_cost, 15006)
        self.assertEqual(table.planned_salary, 2800)
        self.assertEqual(table.planned_other_expenses, 2000)
        self.assertEqual(table.planned_buying_music, 2000)
        self.assertEqual(table.planned_travel_expenses, 2000)
        self.assertEqual(table.planned_fare, 2000)
        self.assertEqual(table.planned_taxes_FOT, 1400)
        self.assertEqual(table.planned_general_expenses, 2806)

        self.assertEqual(table.planned_profit, 134994)
        self.assertEqual(table.planned_profitability, 89.996)

    def test_delete_table(self):
        self.client.post(self.url_table, {"planed_actors_salary": 2000,
                                          "planned_other_expenses": 2000,
                                          "planned_buying_music": 2000,
                                          "planned_travel_expenses": 2000,
                                          "planned_fare": 2000})
        table = self.card.table.get(planed_actors_salary=2000)
        url_table_detail = reverse('table_planned_detail',
                                   kwargs={'card_pk': self.card.pk,
                                           'table_pk': table.pk})
        response = self.client.delete(url_table_detail)
        self.assertEqual(self.card.table.count(), 0)
        self.assertEqual(response.status_code, 200)
