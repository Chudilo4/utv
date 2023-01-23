from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/profile/avatar/', null=True,
                               default='media/profile/avatar/Default_ava.png')

    def __str__(self):
        return self.user.username


class Cards(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    performers = models.ManyToManyField(User, related_name='CardEvent', blank=True)
    date_dedlain = models.DateTimeField()

    def __str__(self):
        return self.title


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


class Worker(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    actual_time = models.TimeField(verbose_name='Фактическое время', default=0)
    scheduled_time = models.TimeField(verbose_name='Плановое время', default=0)