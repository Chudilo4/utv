from rest_framework import serializers
from utv_smeta.models import *


class UserRegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ("id", "username", "password" )


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", 'first_name', 'last_name')


class CommentsSerializers(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comments
        fields = ['id', 'author', 'card', 'text']


class CardsSerializers(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        queryset = Comments.objects.filter(card=obj.pk)
        serializer = CommentsSerializers(queryset, many=True)
        return serializer.data

    class Meta:
        model = Cards
        fields = ['id', 'title', 'author', 'description', 'performers', 'date_dedlain', 'comments']




