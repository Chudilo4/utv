from django.contrib import admin

from utv_api.models import Cards, EmployeeRate


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeRate)
class EmployeeRateAdmin(admin.ModelAdmin):
    pass
