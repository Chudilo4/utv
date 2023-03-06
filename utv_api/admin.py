from utv_api.models import Cards, EmployeeRate, CustomUser
from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeRate)
class EmployeeRateAdmin(admin.ModelAdmin):
    pass
