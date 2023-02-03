from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy, reverse
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

    def get_absolute_url(self):
        return reverse('card_detail' , kwargs={'pk': self.pk})


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Поле для коментария')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)


class Worker(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    actual_time = models.IntegerField(verbose_name='Фактическое время', default=0)
    scheduled_time = models.IntegerField(verbose_name='Плановое время', default=0)

    def get_absolute_url(self):
        return reverse('worker_create', kwargs={'pk': self.pk})

    def __str__(self):
        return self.author.username + ' ' + self.card.title
