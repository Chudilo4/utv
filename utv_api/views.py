from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from utv_smeta.models import *
from utv_api.serializers import UserReadSerializer, CardListSerializers, CardCreateserializers, CardDetailSerializer
from utv_smeta.service import CardService


# Create your views here.


class UsersReadAPIView(APIView):

    def get(self, request, format=None):
        snippets = CustomUser.objects.all()
        serializer = UserReadSerializer(snippets, many=True)
        return Response(serializer.data)


class CardsListAPIView(APIView):
    def get(self, request, format=None):
        data = CardService(author=request.user.pk).my_cards()
        serializer = CardListSerializers(instance=data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CardCreateserializers(data=request.data)
        print(serializer)
        if serializer.is_valid():
            CardService(author=request.user.pk, **serializer.data).create_card()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CardsDetailAPIView(APIView):
    def get(self, request, card_pk, format=None):
        card = CardService(card_pk=card_pk).give_me_card()
        serializer = CardDetailSerializer(instance=card)
        return Response(serializer.data)




