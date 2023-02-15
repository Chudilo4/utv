from rest_framework import serializers

from utv_smeta.models import Cards, Comments, TableProject


class UserReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    avatar = serializers.ImageField()


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'author', 'text']


class TableSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableProject
        fields = '__all__'


class CardDetailSerializer(serializers.ModelSerializer):
    comment = CommentsSerializers(many=True)
    performers = UserReadSerializer(many=True)

    class Meta:
        model = Cards
        fields = ['id', 'author', 'title', 'description', 'created_time', 'performers', 'deadline', 'comment', 'table', 'worker']


class CardListSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserReadSerializer()
    title = serializers.CharField()
    description = serializers.CharField()
    created_time = serializers.DateTimeField()
    performers = UserReadSerializer(many=True)
    deadline = serializers.DateTimeField()
    update_time = serializers.DateTimeField()


class CardCreateserializers(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ['title', 'description', 'performers', 'date_dedlain']





