from rest_framework import serializers
from utv_smeta.models import *


class UserReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "username"]


class ProfileUserSerializer(serializers.ModelSerializer):
    user = UserReadSerializers()

    class Meta:
        model = ProfileUser
        fields = ['id', 'avatar', 'user']


class CommentsSerializers(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comments
        fields = ['id', 'card', 'text']


class CardsSerializers(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    performers = ProfileUserSerializer(many=True)

    class Meta:
        model = Cards
        fields = '__all__'


class WorkerSerializers(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Worker
        fields = '__all__'



