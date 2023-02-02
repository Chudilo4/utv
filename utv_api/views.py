from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from utv_smeta.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated


# Create your views here.


class CardsAPIView(ModelViewSet):
    serializer_class = CardsSerializers
    permission_classes = (IsAuthenticated,)
    lookup_fields = ['title']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cards.objects.filter(author=self.request.user)
        return Cards.objects.filter(author=None)


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [AllowAny, ]
    serializer_class = UserRegisterSerializers


class UserAPIView(ListModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
