from django.contrib import admin
from utv_smeta.models import Cards, Worker, Comments, EmployeeRate, TableProject


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
