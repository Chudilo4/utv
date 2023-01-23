# Generated by Django 4.1.5 on 2023-01-23 12:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utv_smeta', '0002_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cards',
            name='performers',
            field=models.ManyToManyField(blank=True, related_name='CardEvent', to=settings.AUTH_USER_MODEL),
        ),
    ]