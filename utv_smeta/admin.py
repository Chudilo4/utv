from django.contrib import admin
from utv_smeta.models import *
# Register your models here.

@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    pass