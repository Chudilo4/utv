from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='media/profile/avatar/', null=True,
                               default='media/profile/avatar/Default_ava.png')
