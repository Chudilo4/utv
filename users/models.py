from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='profile/avatar/', null=True,
                               default='profile/avatar/Default_ava.png')
