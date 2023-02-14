from rest_framework import serializers
from django.contrib.auth.models import User

from utv_smeta.models import Cards, Comments, TableProject, Worker


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class ProfileUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField()
    user = UserSerializer()


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'author', 'text']


class Tableserializers(serializers.ModelSerializer):
    class Meta:
        model = TableProject
        fields = '__all__'


class CardDetailSerializer(serializers.ModelSerializer):
    comment = CommentsSerializers(many=True)
    table = Tableserializers(many=True)
    performers = UserSerializer(many=True)

    class Meta:
        model = Cards
        fields = ['id', 'author', 'title', 'description', 'created', 'performers', 'date_dedlain', 'comment', 'table']


class CardListSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserSerializer()
    title = serializers.CharField()
    description = serializers.CharField()
    created = serializers.DateTimeField()
    performers = UserSerializer(many=True, read_only=True)
    date_dedlain = serializers.DateTimeField()
    update = serializers.DateTimeField()

class CardCreateserializers(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    performers = UserSerializer(many=True)
    date_dedlain = serializers.DateTimeField()






