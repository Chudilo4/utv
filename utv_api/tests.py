from django.urls import reverse, reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import CustomUser
from utv_smeta.models import Cards


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('users_list')
        data = {'username': 'Nikita',
                'password': '123456789Zz',
                'first_name': 'Artem',
                'last_name': 'Bochkarev',
                }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 0)
        response_post = self.client.post(url, data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.get(username='Nikita').username, 'Nikita')
        self.assertEqual(CustomUser.objects.count(), 1)


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
        url = reverse('cards_detail', kwargs={'card_pk':card.pk})
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), 11)
        response_delete = self.client.delete(url)
        self.assertEqual(Cards.objects.count(), 0)
        self.assertEqual(response_delete.status_code, 200)

    def test_update_card(self):
        user = CustomUser.objects.create_user('Artem', password='123456789Zz')
        user2 = CustomUser.objects.create_user('Nikita', password='123456789Zz')
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
        self.url = reverse('comment_create', kwargs={'card_pk': self.card.pk})

    def test_create_comment(self):
        response = self.client.post(self.url, {"text": "Тест коментария"})
        self.assertEqual(self.card.comment.get(text="Тест коментария").text, "Тест коментария")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)

    def test_delete_comment(self):
        self.client.post(self.url, {"text": "Тест коментария"})
        self.assertEqual(self.card.comment.count(), 1)
        com_pk = self.card.comment.get(text="Тест коментария").pk
        response = self.client.delete(path=reverse('comment_detail', kwargs={'card_pk': self.card.pk,
                                                                             'com_pk': com_pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.card.comment.count(), 0)




