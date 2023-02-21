from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CardsAdmin(admin.ModelAdmin):
    pass
