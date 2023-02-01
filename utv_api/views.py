from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from utv_smeta.models import *
from .serializers import *
# Create your views here.


class CardsAPIListView(ListCreateAPIView):
    serializer_class = CardsSerializers

    def get_queryset(self):
        return Cards.objects.filter(author=self.request.user)


class CardsAPICreateView(CreateAPIView):
    serializer_class = CardsCreateSerializer
    queryset = Cards.objects.all()


class WorkerAPIListView(ListAPIView):
    serializer_class = WorkerSerializers

    def get_queryset(self):
        return Worker.objects.filter(author=self.request.user)


class ProfileUserListView(ListAPIView):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer


