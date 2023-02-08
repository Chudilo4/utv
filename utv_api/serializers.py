from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class ProfileUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField()
    user = UserSerializer()


class CardsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = UserSerializer()
    title = serializers.CharField()
    description = serializers.CharField()
    created = serializers.DateTimeField()
    performers = UserSerializer(many=True)
    date_dedlain = serializers.DateTimeField()





