from utv_api.models import Cards, EmployeeRate, CustomUser, CategoryEvent, Event
from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'description', "created_time",
                    'deadline', 'update_time']
    list_max_show_all = 10
    ordering = ["-created_time"]


@admin.register(EmployeeRate)
class EmployeeRateAdmin(admin.ModelAdmin):
    list_display = ['user', 'money', 'created_time', 'update_time']
    list_max_show_all = 10
    ordering = ["-created_time"]


@admin.register(CategoryEvent)
class CategoryEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_max_show_all = 10


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'date_begin',
                    'data_end', 'category']
    list_max_show_all = 10
    ordering = ["-created_time"]
