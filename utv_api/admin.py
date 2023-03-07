from utv_api.models import Cards, EmployeeRate, CustomUser
from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'description', "created_time",
                    'deadline', 'update_time']
    search_fields = ['author', 'title', 'created_time']
    list_max_show_all = 10
    ordering = ["-created_time"]


@admin.register(EmployeeRate)
class EmployeeRateAdmin(admin.ModelAdmin):
    list_display = ['user', 'money', 'created_time', 'update_time']
    search_fields = ['user']
    list_max_show_all = 10
    ordering = ["-created_time"]
