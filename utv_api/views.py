from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from utv_smeta.models import *
from .serializers import *


# Create your views here.


class UsersAPIView(APIView):

    def get(self, request, format=None):
        snippets = ProfileUser.objects.all()
        serializer = ProfileUserSerializer(snippets, many=True)
        return Response(serializer.data)


class CardsAPIView(APIView):
    def get(self, request, format=None):
        cards = Cards.objects.all()
        serializer = CardsSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CardsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TestApiView(APIView):
#
#     def post(self,request):
#         data = request.body
#         serialser = TestSerailizer(data=data)
#         if not serialser.is_valid():
#             return REspo
#
#         result = Persons().create_user(serialser.data)
#         if result:
#             return Respo()



