from rest_framework import serializers

from users.models import CustomUser
from utv_smeta.models import Cards, Comments, TableProject, Worker


class UserReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    avatar = serializers.ImageField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserCreateSerializers(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        max_length=256
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password', 'avatar']


class UserDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password', 'avatar']


class TableListSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    price_client = serializers.FloatField()
    planned_cost = serializers.FloatField()
    cost = serializers.FloatField()
    planned_salary = serializers.FloatField()
    salary = serializers.FloatField()
    planed_actors_salary = serializers.FloatField()
    actors_salary = serializers.FloatField()
    planned_taxes_FOT = serializers.FloatField()
    taxes_FOT = serializers.FloatField()
    planned_other_expenses = serializers.FloatField()
    other_expenses = serializers.FloatField()
    planned_buying_music = serializers.FloatField()
    buying_music = serializers.FloatField()
    planned_travel_expenses = serializers.FloatField()
    travel_expenses = serializers.FloatField()
    planned_fare = serializers.FloatField()
    fare = serializers.FloatField()
    planned_general_expenses = serializers.FloatField()
    general_expenses = serializers.FloatField()
    planned_profit = serializers.FloatField()
    profit = serializers.FloatField()
    planned_profitability = serializers.FloatField()
    profitability = serializers.FloatField()
    created_time = serializers.DateTimeField()
    updated_time = serializers.DateTimeField()


class TableCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableProject
        fields = ['planed_actors_salary', 'planned_other_expenses', 'planned_buying_music',
                  'planned_travel_expenses', 'planned_fare']


class TableUpdatePlannedSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableProject
        fields = ['price_client', 'planed_actors_salary',
                  'planned_other_expenses',
                  'planned_buying_music',
                  'planned_travel_expenses',
                  'planned_fare']


class TableUpdateFactSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableProject
        fields = ['price_client', 'actors_salary',
                  'other_expenses',
                  'buying_music',
                  'travel_expenses',
                  'fare']


class WorkerListSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserReadSerializer()
    actual_time = serializers.IntegerField()
    scheduled_time = serializers.IntegerField()
    created_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()


class WorkerDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['actual_time', 'scheduled_time']


class WorkerCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['actual_time', 'scheduled_time']


class CommentsSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserReadSerializer()
    text = serializers.CharField()


class TableSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableProject
        fields = '__all__'


class CardReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserReadSerializer()
    title = serializers.CharField()
    description = serializers.CharField()
    created_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()
    performers = UserReadSerializer(many=True, read_only=True)
    deadline = serializers.DateTimeField()


class CardDetailSerializer(serializers.ModelSerializer):
    author = UserReadSerializer()
    comment = CommentsSerializers(many=True)
    performers = UserReadSerializer(many=True)
    worker = WorkerListSerializers(many=True)
    table = TableListSerializers(many=True)

    class Meta:
        model = Cards
        fields = ['id', 'author', 'title', 'description',
                  'created_time', 'update_time', 'performers',
                  'deadline', 'comment', 'table', 'worker']


class CardDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ['title', 'description', 'performers', 'deadline']


class CardListSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserReadSerializer()
    title = serializers.CharField()
    description = serializers.CharField()
    created_time = serializers.DateTimeField()
    performers = UserReadSerializer(many=True)
    deadline = serializers.DateTimeField()
    update_time = serializers.DateTimeField()


class CardCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ['title', 'description', 'performers', 'deadline']


class CommentListSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    author = UserReadSerializer()


class CommentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['text']


class CommentDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['text']
