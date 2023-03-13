from rest_framework import serializers

from utv_api.models import (
    Cards,
    Comments,
    TableProject,
    Worker,
    TableExcel,
    CustomUser,
    CategoryEvent,
    Event)


class UserReadSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'avatar', 'first_name', 'last_name']


class UserCreateSerializers(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        max_length=14,
        min_length=4
    )
    avatar = serializers.ImageField()

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
    planned_actors_salary = serializers.FloatField()
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
    planned_actors_salary = serializers.FloatField(allow_null=False)
    planned_other_expenses = serializers.FloatField(allow_null=False)
    planned_buying_music = serializers.FloatField(allow_null=False)
    planned_travel_expenses = serializers.FloatField(allow_null=False)
    planned_fare = serializers.FloatField(allow_null=False)

    class Meta:
        model = TableProject
        fields = ['planned_actors_salary', 'planned_other_expenses', 'planned_buying_music',
                  'planned_travel_expenses', 'planned_fare']


class TableUpdatePlannedSerializers(serializers.ModelSerializer):
    price_client = serializers.FloatField(allow_null=False)
    planned_actors_salary = serializers.FloatField(allow_null=False)
    planned_other_expenses = serializers.FloatField(allow_null=False)
    planned_buying_music = serializers.FloatField(allow_null=False)
    planned_travel_expenses = serializers.FloatField(allow_null=False)
    planned_fare = serializers.FloatField(allow_null=False)

    class Meta:
        model = TableProject
        fields = ['price_client', 'planned_actors_salary',
                  'planned_other_expenses',
                  'planned_buying_music',
                  'planned_travel_expenses',
                  'planned_fare']


class TableUpdateFactSerializers(serializers.ModelSerializer):
    price_client = serializers.FloatField(allow_null=False)
    actors_salary = serializers.FloatField(allow_null=False)
    other_expenses = serializers.FloatField(allow_null=False)
    buying_music = serializers.FloatField(allow_null=False)
    travel_expenses = serializers.FloatField(allow_null=False)
    fare = serializers.FloatField(allow_null=False)

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
    actual_time = serializers.IntegerField(min_value=0, allow_null=False)
    scheduled_time = serializers.IntegerField(min_value=0, allow_null=False)

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
    archived = serializers.BooleanField()


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
                  'deadline', 'comment', 'table', 'worker',
                  'archived']


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


class ExcelSerializer(serializers.ModelSerializer):
    path_excel = serializers.FileField(use_url=True)

    class Meta:
        model = TableExcel
        fields = ['id', 'name', 'table', 'path_excel', 'created_time']


class ExcelCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class CategoryEventListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class CategoryEventAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryEvent
        fields = '__all__'


class EventListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserReadSerializer()
    title = serializers.CharField(max_length=255, min_length=3, allow_blank=False)
    date_begin = serializers.DateTimeField()
    data_end = serializers.DateTimeField()
    category = CategoryEventListSerializer()
    performers = UserReadSerializer(many=True)


class EventAddSerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=False)
    date_begin = serializers.DateTimeField(allow_null=False)
    data_end = serializers.DateTimeField(allow_null=False)
    category = serializers.IntegerField(allow_null=False)

    class Meta:
        model = Event
        fields = ['title', 'date_begin', 'data_end', 'category', 'performers']
