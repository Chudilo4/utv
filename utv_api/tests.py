from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from utv_api.models import Cards, Comments, Worker, CustomUser


# class AccountTests(APITestCase):
#
#     def generate_photo_file(self):
#         file = io.BytesIO()
#         image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
#         image.save(file, 'png')
#         file.name = 'test.png'
#         file.seek(0)
#         return file
#
#     def setUp(self):
#         self.url_register = reverse('users_register')
#         self.url_users = reverse('users_list')
#         self.url_put = reverse('users_detail', kwargs={'user_pk': 1})
#         self.data = {'username': 'Nikita',
#                      'password': '123456789Zz',
#                      'first_name': 'Nikita',
#                      'last_name': 'Metelev',
#                      'avatar': self.generate_photo_file()
#                      }
#         self.data2 = {'username': 'Artem',
#                       'password': '123456789Zz',
#                       'first_name': 'Artem',
#                       'last_name': 'Tue',
#                       'avatar': self.generate_photo_file()
#                       }
#
#     def test_create_account(self):
#         """
#         Тест на создание пользователя
#         """
#         response = self.client.get(self.url_users)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(CustomUser.objects.count(), 0)
#         response_post = self.client.post(self.url_register, self.data)
#         self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(CustomUser.objects.get(username='Nikita').username, 'Nikita')
#         self.assertEqual(CustomUser.objects.count(), 1)
#
#     def test_read_user(self):
#         resp_post = self.client.post(self.url_register, self.data)
#         self.assertEqual(resp_post.status_code, status.HTTP_201_CREATED)
#         self.client.login(username="Nikita", password='123456789Zz')
#         response = self.client.get(self.url_users)
#         self.assertEqual(CustomUser.objects.all().count(), 1)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         resp = self.client.get(self.url_put)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#
#     def test_update_user(self):
#         """Тест на изменения аккаунта пользователя"""
#         resp_post = self.client.post(self.url_register, self.data)
#         self.assertEqual(resp_post.status_code, status.HTTP_201_CREATED)
#         self.client.login(username='Nikita', password='123456789Zz')
#         response = self.client.put(self.url_put, self.data2)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(CustomUser.objects.get(pk=1).username, "Artem")
#
#     def test_delete_user(self):
#         url_delete = reverse('users_detail', kwargs={'user_pk': 1})
#         self.client.post(self.url_register, self.data)
#         self.client.post(self.url_register, self.data2)
#         self.assertEqual(CustomUser.objects.all().count(), 2)
#         self.client.login(username='Nikita', password='123456789Zz')
#         response = self.client.delete(url_delete)
#         self.assertEqual(CustomUser.objects.all().count(), 1)
#         self.assertEqual(response.status_code, 200)
#
#
# class CardTests(APITestCase):
#     def test_create_card(self):
#         url = reverse('cards_list')
#         data = {
#             "title": "Тестовая карточка",
#             "description": "Описание для тестовой карточки",
#             'performers': [1],
#             "deadline": "2023-02-28T12:00:00+05:00",
#         }
#         CustomUser.objects.create_user('Artem', password='123456789Zz')
#         self.client.login(username='Artem', password='123456789Zz')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Cards.objects.count(), 0)
#         response2 = self.client.post(url, data)
#         self.assertEqual(Cards.objects.count(), 1)
#         self.assertEqual(Cards.objects.get(title="Тестовая карточка").title, 'Тестовая карточка')
#         self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
#
#     def test_delete_card(self):
#         CustomUser.objects.create_user('Artem', password='123456789Zz')
#         data = {
#             "title": "Тестовая карточка",
#             "description": "Описание для тестовой карточки",
#             "deadline": "2023-02-28T12:00:00+05:00",
#             'performers': [1]
#         }
#         self.client.login(username='Artem', password='123456789Zz')
#         self.client.post(reverse('cards_list'), data)
#         url = reverse('cards_detail', kwargs={'card_pk': 1})
#         response_delete = self.client.delete(url)
#         self.assertEqual(Cards.objects.count(), 0)
#         self.assertEqual(response_delete.status_code, 200)
#
#     def test_update_card(self):
#         CustomUser.objects.create_user('Artem', password='123456789Zz')
#         CustomUser.objects.create_user('Nikita', password='123456789Zz')
#         data = {
#             "title": "Тестовая карточка",
#             "description": "Описание для тестовой карточки",
#             "deadline": "2023-02-28T12:00:00+05:00",
#             'performers': [1, 2]
#         }
#         data2 = {
#             "title": "Тестовая карточкацуцацац",
#             "description": "Описание для тестовой карточкиqwe",
#             "deadline": '2023-02-28T12:00:00+05:00',
#             'performers': [1, 2]
#         }
#         self.client.login(username='Artem', password='123456789Zz')
#         self.client.post(reverse('cards_list'), data)
#         self.assertEqual(Cards.objects.count(), 1)
#         url = reverse('cards_detail', kwargs={'card_pk': 1})
#         response = self.client.put(url, data2, format='json')
#         self.assertEqual(response.status_code, 200)
#
#     def test_read_card(self):
#         user = CustomUser.objects.create_user(username='Artem',
#                                               first_name='Artem',
#                                               last_name="Bockarev")
#         user.set_password('123456789Zz')
#         user.save()
#         card = Cards.objects.create(author=user,
#                                     title="Тестовая карточкацуцацац",
#                                     description="Описание для тестовой карточкиqwe",
#                                     deadline="2023-02-28T12:00:00+05:00",
#                                     )
#         card.performers.add(user)
#         self.client.login(username='Artem', password='123456789Zz')
#         url = reverse('cards_list')
#         response_get = self.client.get(url)
#         self.assertEqual(response_get.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response_get.data), 1)
#
#
# class CommentTests(APITestCase):
#     def setUp(self):
#         user = CustomUser.objects.create_user('Artem', password='123456789Zz')
#         self.card = Cards.objects.create(author=user,
#                                          title="Тестовая карточкацуцацац",
#                                          description="Описание для тестовой карточкиqwe",
#                                          deadline="2023-02-28T12:00:00+05:00",
#                                          )
#         self.card.performers.add(user)
#         self.client.login(username='Artem', password='123456789Zz')
#         self.url = reverse('comment_list', kwargs={'card_pk': self.card.pk})
#
#     def test_create_comment(self):
#         response = self.client.post(self.url, {"text": "Тест коментария"})
#         self.assertEqual(Comments.objects.get(text="Тест коментария").text, "Тест коментария")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_delete_comment(self):
#         self.client.post(self.url, {"text": "Тест коментария"})
#         self.assertEqual(Comments.objects.all().count(), 1)
#         com_pk = Comments.objects.get(text="Тест коментария").pk
#         response = self.client.delete(
#             path=reverse('comment_detail', kwargs={'card_pk': self.card.pk,
#                                                    'com_pk': com_pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Comments.objects.filter(card_id=self.card.pk).count(), 0)
#
#     def test_update_comment(self):
#         self.client.post(self.url, {"text": "Тест коментария"})
#         com_pk = Comments.objects.get(text="Тест коментария").pk
#         response_put = self.client.put(reverse('comment_detail',
#                                                kwargs={
#                                                    "card_pk": self.card.pk,
#                                                    'com_pk': com_pk}),
#                                        {"text": "Тест коментарияйцу"})
#         self.assertEqual(response_put.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             Comments.objects.get(pk=com_pk).text, 'Тест коментарияйцу')
#         self.assertEqual(Comments.objects.all().count(), 1)
#
#     def test_read_comment(self):
#         self.client.post(self.url, {"text": "Тест коментария"})
#         self.client.post(self.url, {"text": "Тест коментария"})
#         response_get = self.client.get(self.url)
#         self.assertEqual(response_get.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response_get.data), 2)
#         response_get_detail = self.client.get(reverse('comment_detail',
#                                                       kwargs={
#                                                           "card_pk": self.card.pk,
#                                                           'com_pk': 1}
#                                                       ))
#         self.assertEqual(response_get_detail.status_code, status.HTTP_200_OK)
#
#
# class WorkerTests(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user('Artem', password='123456789Zz')
#         self.card = Cards.objects.create(author=self.user,
#                                          title="Тестовая карточкацуцацац",
#                                          description="Описание для тестовой карточкиqwe",
#                                          deadline="2023-02-28T12:00:00+05:00",
#                                          )
#         self.card.performers.add(self.user)
#         self.client.login(username='Artem', password='123456789Zz')
#         self.url = reverse('worker_list', kwargs={'card_pk': self.card.pk})
#
#     def test_create_worker(self):
#         response = self.client.post(self.url, {"actual_time": 5,
#                                                "scheduled_time": 4})
#         self.assertEqual(Worker.objects.all().count(), 1)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Worker.objects.get(author=self.user).actual_time, 5)
#         self.assertEqual(Worker.objects.get(author=self.user).scheduled_time, 4)
#
#     def test_update_worker(self):
#         self.client.post(self.url, {"actual_time": 5,
#                                     "scheduled_time": 4})
#         w = Worker.objects.get(author=self.user)
#         url = reverse('worker_detail', kwargs={'card_pk': self.card.pk,
#                                                'work_pk': w.pk})
#         response = self.client.put(url,
#                                    '{"actual_time": 3, "scheduled_time": 3}',
#                                    content_type='application/json')
#         self.assertEqual(Worker.objects.all().count(), 1)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Worker.objects.get(author=self.user).actual_time, 3)
#         self.assertEqual(Worker.objects.get(author=self.user).scheduled_time, 3)
#
#     def test_delete_work(self):
#         self.client.post(self.url, {"actual_time": 5,
#                                     "scheduled_time": 4})
#         w = Worker.objects.get(author=self.user)
#         url = reverse('worker_detail', kwargs={'card_pk': self.card.pk,
#                                                'work_pk': w.pk})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Worker.objects.all().count(), 0)
#
#     def test_read_work(self):
#         self.client.post(self.url, {"actual_time": 5,
#                                     "scheduled_time": 4})
#         response = self.client.get(reverse('worker_list',
#                                            kwargs={"card_pk": self.card.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         response2 = self.client.get(reverse('worker_detail', kwargs={"work_pk": 1,
#                                                                      "card_pk": self.card.pk}))
#         self.assertEqual(response2.status_code, status.HTTP_200_OK)
#
#
# class TableTests(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user('ArtemTEST', password='123456789Zz')
#         EmployeeRate.objects.create(user=self.user, money=200)
#         data = {
#             "title": "Тестовая карточка",
#             "description": "Описание для тестовой карточки",
#             'performers': [1],
#             "deadline": "2023-02-28T12:00:00+05:00",
#         }
#         self.client.login(username='ArtemTEST', password='123456789Zz')
#         self.url_card = reverse('cards_list')
#         self.client.post(self.url_card, data)
#         self.card = Cards.objects.get(title="Тестовая карточка")
#         self.url_worker = reverse('worker_list', kwargs={'card_pk': self.card.pk})
#         self.url_comment = reverse('comment_list', kwargs={'card_pk': self.card.pk})
#         self.url_table = reverse('table_list', kwargs={"card_pk": self.card.pk})
#         self.client.post(self.url_comment, {"text": "Тест коментария"})
#         self.client.post(self.url_worker, {"actual_time": 4, "scheduled_time": 4})
#
#     def test_created_table(self):
#         response = self.client.post(self.url_table, {"planned_actors_salary": 2000,
#                                                      "planned_other_expenses": 2000,
#                                                      "planned_buying_music": 2000,
#                                                      "planned_travel_expenses": 2000,
#                                                      "planned_fare": 2000})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(TableProject.objects.all().count(), 1)
#
#     def test_update_table(self):
#         self.client.post(self.url_table, {"planned_actors_salary": 2000,
#                                           "planned_other_expenses": 2000,
#                                           "planned_buying_music": 2000,
#                                           "planned_travel_expenses": 2000,
#                                           "planned_fare": 2000})
#         table = TableProject.objects.get(pk=1)
#         url_table_planned = reverse('table_update_planned',
#                                     kwargs={'card_pk': self.card.pk,
#                                             'table_pk': table.pk})
#         url_table_fact = reverse('table_update_fact',
#                                  kwargs={'card_pk': self.card.pk,
#                                          'table_pk': table.pk})
#         response = self.client.put(url_table_planned, {
#             "planned_actors_salary": 2000,
#             "planned_other_expenses": 2000,
#             "planned_buying_music": 2000,
#             "planned_travel_expenses": 2000,
#             "planned_fare": 2000,
#             "price_client": 150000
#         }, format='json')
#         response2 = self.client.put(url_table_fact, {
#             "actors_salary": 2000,
#             "other_expenses": 2000,
#             "buying_music": 2000,
#             "travel_expenses": 2000,
#             "fare": 2000,
#             "price_client": 150000
#         }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response2.status_code, status.HTTP_200_OK)
#         self.assertEqual(TableProject.objects.all().count(), 1)
#         table = TableProject.objects.get(price_client=150000)
#         self.assertEqual(table.planned_cost, 15006)
#         self.assertEqual(table.cost, 15006)
#         self.assertEqual(table.planned_salary, 2800)
#         self.assertEqual(table.salary, 2800)
#         self.assertEqual(table.planned_other_expenses, 2000)
#         self.assertEqual(table.other_expenses, 2000)
#         self.assertEqual(table.planned_buying_music, 2000)
#         self.assertEqual(table.buying_music, 2000)
#         self.assertEqual(table.planned_travel_expenses, 2000)
#         self.assertEqual(table.travel_expenses, 2000)
#         self.assertEqual(table.planned_fare, 2000)
#         self.assertEqual(table.fare, 2000)
#         self.assertEqual(table.planned_taxes_FOT, 1400)
#         self.assertEqual(table.taxes_FOT, 1400)
#         self.assertEqual(table.planned_general_expenses, 2806)
#         self.assertEqual(table.general_expenses, 2806)
#         self.assertEqual(table.planned_profit, 134994)
#         self.assertEqual(table.profit, 134994)
#         self.assertEqual(table.planned_profitability, 89.996)
#         self.assertEqual(table.profitability, 89.996)
#
#     def test_read_table(self):
#         self.client.post(self.url_table, {"planned_actors_salary": 2000,
#                                           "planned_other_expenses": 2000,
#                                           "planned_buying_music": 2000,
#                                           "planned_travel_expenses": 2000,
#                                           "planned_fare": 2000})
#         response = self.client.get(reverse('table_detail', kwargs={"table_pk": 1,
#                                                                    'card_pk': self.card.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_delete_table(self):
#         self.client.post(self.url_table, {"planned_actors_salary": 2000,
#                                           "planned_other_expenses": 2000,
#                                           "planned_buying_music": 2000,
#                                           "planned_travel_expenses": 2000,
#                                           "planned_fare": 2000})
#         table = TableProject.objects.get(pk=1)
#         url_table_detail = reverse('table_detail',
#                                    kwargs={'card_pk': self.card.pk,
#                                            'table_pk': table.pk})
#         response = self.client.delete(url_table_detail)
#         self.assertEqual(TableProject.objects.all().count(), 0)
#         self.assertEqual(response.status_code, 200)
#
#
# class TestPermissions(APITestCase):
#     def setUp(self) -> None:
#         user = CustomUser.objects.create_user('Artem', password='123456789Zz')
#         EmployeeRate.objects.create(user=user, money=200)
#         data = {
#             "title": "Тестовая карточка",
#             "description": "Описание для тестовой карточки",
#             'performers': [],
#             "deadline": "2023-02-28T12:00:00+05:00",
#         }
#         self.data2 = {
#             "title": "Тестовая карточкаffff",
#             "description": "Описание для тестовой карточки",
#             'performers': [],
#             "deadline": "2023-02-28T12:00:00+05:00",
#         }
#         self.client.login(username='Artem', password='123456789Zz')
#         self.url_card = reverse('cards_list')
#         self.client.post(self.url_card, data)
#         self.card = Cards.objects.get(title="Тестовая карточка")
#         self.url_worker = reverse('worker_list', kwargs={'card_pk': self.card.pk})
#         self.url_comment = reverse('comment_list', kwargs={'card_pk': self.card.pk})
#         self.url_table = reverse('table_list', kwargs={"card_pk": self.card.pk})
#         self.url_card_detail = reverse('cards_detail', kwargs={'card_pk': self.card.pk})
#         self.client.post(self.url_comment, {"text": "Тест коментария"})
#         self.client.post(self.url_worker, {"actual_time": 4, "scheduled_time": 4})
#         self.client.post(self.url_table, {"planned_actors_salary": 2000,
#                                           "planned_other_expenses": 2000,
#                                           "planned_buying_music": 2000,
#                                           "planned_travel_expenses": 2000,
#                                           "planned_fare": 2000})
#         self.table = TableProject.objects.get(pk=1)
#         self.url_table_detail = reverse('table_detail',
#                                         kwargs={
#                                             'card_pk': self.card.pk,
#                                             'table_pk': self.table.pk
#                                         })
#         self.client.logout()
#
#     def test_not_permission(self):
#         table_post_data = {
#             "planned_actors_salary": 2000,
#             "planned_other_expenses": 2000,
#             "planned_buying_music": 2000,
#             "planned_travel_expenses": 2000,
#             "planned_fare": 2000
#         }
#         CustomUser.objects.create_user('Nikita', password='123456789Zz')
#         self.client.login(username='Nikita',
#                           password='123456789Zz')
#         # Проверка на доуступ к карточке
#         get_detail_card = self.client.get(
#             reverse('cards_detail', kwargs={'card_pk': self.card.pk}))
#         self.assertEqual(get_detail_card.status_code, status.HTTP_403_FORBIDDEN)
#         # Првоерка доступа на удаление карточки
#         delete_card = self.client.delete(self.url_card_detail)
#         self.assertEqual(delete_card.status_code, status.HTTP_403_FORBIDDEN)
#         # Проверка на изменение карточки
#         put_card = self.client.put(self.url_card_detail, self.data2)
#         self.assertEqual(put_card.status_code, status.HTTP_403_FORBIDDEN)
#         # Проверка на чтение коментаторов
#         get_comments_card = self.client.get(
#             reverse('comment_list', kwargs={"card_pk": self.card.pk})
#         )
#         self.assertEqual(get_comments_card.status_code, status.HTTP_403_FORBIDDEN)
#         # Проверка на изменение коментария
#         post_comment = self.client.post(reverse('comment_list', kwargs={"card_pk": self.card.pk}))
#         self.assertEqual(post_comment.status_code, status.HTTP_403_FORBIDDEN)
#         # Проверка на удаление комментария
#         delete_comment = self.client.delete(reverse('comment_detail',
#                                                     kwargs={
#                                                         "card_pk": 1,
#                                                         "com_pk": 1
#                                                     }))
#         self.assertEqual(delete_comment.status_code, status.HTTP_403_FORBIDDEN)
#         # Проверка на изменение комментария
#         put_comment = self.client.put(reverse('comment_detail',
#                                               kwargs={
#                                                   "card_pk": 1,
#                                                   "com_pk": 1
#                                               }))
#         self.assertEqual(put_comment.status_code, status.HTTP_403_FORBIDDEN)
#         # # Проверка на изменение пользователя
#         # put_user = self.client.put(reverse("users_detail", kwargs={
#         #     "user_pk": 1
#         # }))
#         # self.assertEqual(put_user.status_code, status.HTTP_403_FORBIDDEN)
#         # # Проверка на удаление пользователя
#         # delete_user_detail = self.client.delete(reverse('users_detail',
#         #                                                 kwargs={'user_pk': self.user.pk}))
#         # self.assertEqual(delete_user_detail.status_code, status.HTTP_403_FORBIDDEN)
#         # Проверка на доступ к списку таблиц
#         get_table_list = self.client.get(self.url_table)
#         self.assertEqual(get_table_list.status_code, status.HTTP_403_FORBIDDEN)
#         # Создание таблицы
#         post_table = self.client.post(self.url_table, data=table_post_data)
#         self.assertEqual(post_table.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(TableProject.objects.all().count(), 1)
#         # Проверка на доступ к таблице
#         get_table_detail = self.client.get(self.url_table_detail)
#         self.assertEqual(get_table_detail.status_code, status.HTTP_403_FORBIDDEN)
#         # Проверка на удаление таблицы
#         delete_table = self.client.delete(self.url_table_detail)
#         self.assertEqual(delete_table.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(TableProject.objects.all().count(), 1)
#         # Проверка на создание работы в карточке где пользователь не учавствует
#         post_work = self.client.post(self.url_worker, {"actual_time": 4, "scheduled_time": 4})
#         self.assertEqual(post_work.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(Worker.objects.all().count(), 1)
#         # Проверка на изменение чужой работы
#         put_work = self.client.put(self.url_worker, {"actual_time": 5, "scheduled_time": 5})
#         self.assertEqual(put_work.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(Worker.objects.all().count(), 1)
#         # Проверка на удаление работы
#         delete_work = self.client.delete(self.url_worker)
#         self.assertEqual(delete_work.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(Worker.objects.all().count(), 1)


class TestCards(APITestCase):

    def setUp(self) -> None:
        self.user_owner = CustomUser.objects.create_user('Artem', password='123456789Zz')
        self.user_performer = CustomUser.objects.create_user('Nikita', password='123456789Zz')
        self.user_renegade = CustomUser.objects.create_user('Rafa', password='123456789Zz')
        self.user_new_performer = CustomUser.objects.create_user('Ruslan', password='123456789Zz')
        self.card = Cards.objects.create(title='Мой проект',
                                         description='Моё описание',
                                         deadline=timezone.now(),
                                         author=self.user_owner)
        self.card.performers.add(self.user_performer.pk,
                                 self.user_owner.pk)
        self.url_card_detail = reverse('cards_detail', kwargs={'card_pk': 1})
        self.url_cards = reverse('cards_list')

    def test_no_permission_user_renegade(self):
        """Тест на запрет чтения, изменения и удаления
        карточки если пользователь не исполнитель и не автор"""
        self.client.login(username='Rafa', password='123456789Zz')
        response_card_detail_get = self.client.get(self.url_card_detail)
        response_card_detail_delete = self.client.delete(self.url_card_detail)
        response_card_detail_put = self.client.put(self.url_card_detail,
                                                   {"title": "УДАЛИТЬ",
                                                    "description": "УДАЛИТЬ",
                                                    "deadline": timezone.now(),
                                                    "performers": [self.user_renegade]
                                                    })
        self.assertEqual(response_card_detail_get.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_card_detail_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_card_detail_put.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_permission_user_performer(self):
        """Тест на запрет изменения и удаление карточки если пользователь исполнитель"""
        self.client.login(username='Nikita', password='123456789Zz')
        response_card_detail_put = self.client.put(self.url_card_detail,
                                                   {"title": "Нет мой",
                                                    "description": "Нет моё описание",
                                                    "deadline": timezone.now(),
                                                    })
        response_card_detail_delete = self.client.delete(self.url_card_detail)
        self.assertEqual(response_card_detail_put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Cards.objects.get(pk=1).title, 'Мой проект')
        self.assertEqual(response_card_detail_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Cards.objects.all().count(), 1)

    def test_have_permission_user_performer(self):
        """Тест на чтение карточки если пользователь исполнитель"""
        self.client.login(username='Nikita', password='123456789Zz')
        response_card_detail = self.client.get(self.url_card_detail)
        self.assertEqual(response_card_detail.status_code, status.HTTP_200_OK)

    def test_have_permission_user_owner(self):
        """Тест на чтение, изменение, удаление карточки если пользователь автор карточки"""
        self.client.login(username='Artem', password='123456789Zz')
        response_card_detail_get = self.client.get(self.url_card_detail)
        self.assertEqual(response_card_detail_get.status_code, status.HTTP_200_OK)
        response_card_detail_put = self.client.put(self.url_card_detail,
                                                   {"title": "Новый исполнитель",
                                                    "description": "Добавил нового исполнителя",
                                                    "deadline": timezone.now(),
                                                    "performers": [self.user_new_performer.pk]
                                                    })
        self.assertEqual(response_card_detail_put.status_code, status.HTTP_200_OK)
        self.assertEqual(self.card.performers.all().count(), 3)
        response_card_detail_delete = self.client.delete(self.url_card_detail)
        self.assertEqual(response_card_detail_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(Cards.objects.all().count(), 0)

    def test_have_permission_created_card(self):
        """Тест на создание карточки если пользователь аутентифицирован"""
        self.client.login(username='Ruslan', password='123456789Zz')
        response_card_create = self.client.post(self.url_cards,
                                                {"title": "Новая карточка",
                                                 "description": "Новое описание в новой карточке",
                                                 "deadline": timezone.now(),
                                                 "performers": [self.user_new_performer.pk]
                                                 })
        self.assertEqual(response_card_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cards.objects.get(pk=2).author, self.user_new_performer)
        self.assertEqual(Cards.objects.all().count(), 2)

    def test_no_permission_if_not_login(self):
        """Тест на создание, изменение и удаление карточки если пользователь не аутентифицирован"""
        response_card_create_no_login = self.client.post(
            self.url_cards,
            {"title": "Новая карточка",
             "description": "Новое описание в новой карточке",
             "deadline": timezone.now(),
             "performers": [self.user_new_performer.pk]
             })
        self.assertEqual(response_card_create_no_login.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Cards.objects.all().count(), 1)
        response_card_detail_put = self.client.put(self.url_card_detail,
                                                   {"title": "Новая карточка без логина",
                                                    "description": "Новая карточка без логина",
                                                    "deadline": timezone.now(),
                                                    "performers": [self.user_new_performer.pk]
                                                    })
        self.assertEqual(response_card_detail_put.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Cards.objects.get(pk=1).title, 'Мой проект')
        response_card_detail_delete = self.client.delete(self.url_card_detail)
        self.assertEqual(response_card_detail_delete.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Cards.objects.all().count(), 1)


class TestComment(APITestCase):

    def setUp(self) -> None:
        self.user_owner = CustomUser.objects.create_user('Artem', password='123456789Zz')
        self.user_performer = CustomUser.objects.create_user('Nikita', password='123456789Zz')
        self.user_renegade = CustomUser.objects.create_user('Rafa', password='123456789Zz')
        self.user_new_performer = CustomUser.objects.create_user('Ruslan', password='123456789Zz')
        self.card = Cards.objects.create(title='Мой проект',
                                         description='Моё описание',
                                         deadline=timezone.now(),
                                         author=self.user_owner)
        self.card.performers.add(self.user_performer.pk,
                                 self.user_owner.pk)
        self.url_card_detail = reverse('cards_detail', kwargs={'card_pk': 1})
        self.url_cards = reverse('cards_list')
        self.url_comments = reverse('comment_list', kwargs={'card_pk': 1})
        self.comment_owner = Comments.objects.create(author=self.user_owner,
                                                     card=self.card,
                                                     text='Это коментарий автора карточки')
        self.url_comments_detail = reverse('comment_detail', kwargs={'card_pk': 1,
                                                                     'com_pk': 1})

    def test_no_permission_user_renegade(self):
        """Тест на запрет чтения, и добавления коментария если
        пользователь не автор карточки или участник ,
        а так же на чтение, удаление, изменение комментария
        автором которой он не является"""
        # Чтение  и добавление коментариев в карточке
        self.client.login(username='Rafa', password='123456789Zz')
        response_comment_get = self.client.get(self.url_comments)
        self.assertEqual(response_comment_get.status_code, status.HTTP_403_FORBIDDEN)
        response_comment_post = self.client.post(self.url_comments,
                                                 {
                                                     "text": "Это коментарий ренегата"
                                                 })
        self.assertEqual(response_comment_post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.card.comments_card.all().count(), 1)
        # Чтение, добавление, удаление и изменение коментария в карточке
        response_comment_detail_get = self.client.get(self.url_comments_detail)
        self.assertEqual(response_comment_detail_get.status_code, status.HTTP_403_FORBIDDEN)
        response_comment_put = self.client.put(self.url_comments_detail,
                                               {"text": "Ахахаха я поменял этот коментарий"})
        self.assertEqual(response_comment_put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.comment_owner.text, 'Это коментарий автора карточки')
        response_comment_delete = self.client.delete(self.url_comments_detail)
        self.assertEqual(response_comment_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.card.comments_card.all().count(), 1)

    def test_no_permission_user_performers(self):
        """Тест на запрет удаления и изменения коментария если
        пользователь не является его автором"""
        self.client.login(username='Nikita', password='123456789Zz')
        response_comment_detail_put = self.client.put(self.url_comments_detail,
                                                      {
                                                          "text": "Я поменял твой коммментарий"
                                                      })
        self.assertEqual(response_comment_detail_put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.comment_owner.text, 'Это коментарий автора карточки')
        response_comment_detail_delete = self.client.delete(self.url_comments_detail)
        self.assertEqual(response_comment_detail_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.card.comments_card.all().count(), 1)

    def test_permission_user_performer_or_user_owner_card(self):
        """Тест на добавление коментария и чтение если пользователь исполнитель ,
        а так же изменение, и удаление своего коментария"""
        self.client.login(username='Nikita', password='123456789Zz')
        # Добавление и чтение всех коментариев к карточке
        response_comment_post = self.client.post(self.url_comments,
                                                 {"text": "Это комментарий исполнителя Nikita"})
        self.assertEqual(response_comment_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.card.comments_card.all().count(), 2)
        response_comment_get = self.client.get(self.url_comments)
        self.assertEqual(response_comment_get.status_code, status.HTTP_200_OK)
        # Изменение и удаление своего коментария
        url_comment_performer = reverse('comment_detail', kwargs={"card_pk": 1,
                                                                  "com_pk": 2})
        response_comment_detail_put = self.client.put(url_comment_performer,
                                                      {
                                                          "text": "Я поменял свой комментарий"
                                                      })
        self.assertEqual(response_comment_detail_put.status_code, status.HTTP_200_OK)
        c = Comments.objects.get(author=self.user_performer, card=self.card)
        self.assertEqual(c.text, 'Я поменял свой комментарий')
        response_comment_detail_delete = self.client.delete(url_comment_performer)
        self.assertEqual(response_comment_detail_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(self.card.comments_card.all().count(), 1)


class TestWorker(APITestCase):

    def setUp(self) -> None:
        self.user_owner = CustomUser.objects.create_user('Artem', password='123456789Zz')
        self.user_performer = CustomUser.objects.create_user('Nikita', password='123456789Zz')
        self.user_renegade = CustomUser.objects.create_user('Rafa', password='123456789Zz')
        self.user_new_performer = CustomUser.objects.create_user('Ruslan', password='123456789Zz')
        self.card = Cards.objects.create(title='Мой проект',
                                         description='Моё описание',
                                         deadline=timezone.now(),
                                         author=self.user_owner)
        self.card.performers.add(self.user_performer.pk,
                                 self.user_owner.pk)
        self.url_card_detail = reverse('cards_detail', kwargs={'card_pk': 1})
        self.url_cards = reverse('cards_list')
        self.work = Worker.objects.create(author=self.user_performer,
                                          actual_time=4,
                                          scheduled_time=4,
                                          card=self.card)
        self.url_worker = reverse('worker_list', kwargs={'card_pk': 1})
        self.url_worker_detail = reverse('worker_detail', kwargs={
            'card_pk': 1,
            'work_pk': 1
        })

    def test_no_permission_if_user_not_owner_and_not_performer(self):
        """
        Тест на запрет чтения и добавление рабочего времени
        если пользователь не участник карточки ,
        а так же на детальное чтение удаление и
        изменение рабочего времени участников
        """
        self.client.login(username="Rafa", password='123456789Zz')
        # Тест на получение списка работ
        response_get_worker = self.client.get(self.url_worker)
        self.assertEqual(response_get_worker.status_code, status.HTTP_403_FORBIDDEN)
        # Тест на создание работы
        respone_post_worker = self.client.post(self.url_worker,
                                               {
                                                   "actual_time": 5,
                                                   "scheduled_time": 5
                                               })
        self.assertEqual(respone_post_worker.status_code, status.HTTP_403_FORBIDDEN)
        # Тест на чтение конкретной работы
        response_get_worker_detail = self.client.get(self.url_worker_detail)
        self.assertEqual(response_get_worker_detail.status_code, status.HTTP_403_FORBIDDEN)
        # Тест на изменение рабочки
        response_put_worker_detail = self.client.put(self.url_worker_detail,
                                                     {
                                                         "actual_time": 5,
                                                         "scheduled_time": 5
                                                     })
        self.assertEqual(response_put_worker_detail.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.work.actual_time, 4)
        # Тест на удаление рабочки
        response_delete_worker_detail = self.client.delete(self.url_worker_detail)
        self.assertEqual(response_delete_worker_detail.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Worker.objects.filter(card=self.card).count(), 1)

    def test_permission_change_only_owner(self):
        """Тест на изменение и удаление работы только автором работы"""
        self.client.login(username="Artem", password='123456789Zz')
        # Изменение карточки
        response_put_worker_detail = self.client.put(self.url_worker_detail,
                                                     {
                                                         "actual_time": 5,
                                                         "scheduled_time": 5
                                                     })
        self.assertEqual(response_put_worker_detail.status_code, status.HTTP_403_FORBIDDEN)
        # Удаление карточки
        response_delete_worker_detail = self.client.delete(self.url_worker_detail)
        self.assertEqual(response_delete_worker_detail.status_code, status.HTTP_403_FORBIDDEN)

    def test_have_permission_performer(self):
        self.client.login(username='Nikita', password='123456789Zz')
        response_get_worker_detail = self.client.get(self.url_worker_detail)
        self.assertEqual(response_get_worker_detail.status_code, status.HTTP_200_OK)
        response_put_worker_detail = self.client.put(self.url_worker_detail,
                                                     {
                                                         "actual_time": 5,
                                                         "scheduled_time": 5
                                                     })
        self.assertEqual(response_put_worker_detail.status_code, status.HTTP_200_OK)
        response_delete_worker_detail = self.client.delete(self.url_worker_detail)
        self.assertEqual(response_delete_worker_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(Worker.objects.filter(card=self.card).count(), 0)
