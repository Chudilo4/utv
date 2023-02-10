from django.contrib import admin
from utv_smeta.models import *
# Register your models here.

@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    pass


@admin.register(Worker)
class WorkersAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeRate)
class EmployeeRateAdmin(admin.ModelAdmin):
    pass


@admin.register(TableProject)
class TableProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(SalaryProjectUser)
class SalaryProjectUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_project', 'user', 'planned_salary', 'salary', 'created_time')