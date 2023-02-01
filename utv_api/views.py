from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from utv_smeta.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.


class CardsAPIView(ModelViewSet):
    serializer_class = CardsSerializers
    queryset = Cards.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )


class UserAPIView(ModelViewSet):
    serializer_class = UserListSerializers
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )


# class CardsAPIListView(ListAPIView):
#     serializer_class = CardsSerializers
#
#     def get_queryset(self):
#         return Cards.objects.filter(author=self.request.user)
#
#
# class CardsAPICreateView(CreateAPIView):
#     serializer_class = CardsCreateSerializer
#     queryset = Cards.objects.all()
#
#
# class WorkerAPIListView(ListAPIView):
#     serializer_class = WorkerSerializers
#
#     def get_queryset(self):
#         return Worker.objects.filter(author=self.request.user)
#
#
# class ProfileUserListView(ListAPIView):
#     queryset = ProfileUser.objects.all()
#     serializer_class = ProfileUserSerializer


