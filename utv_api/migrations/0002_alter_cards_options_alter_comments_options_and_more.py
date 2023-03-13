# Generated by Django 4.1.5 on 2023-03-09 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utv_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cards',
            options={'verbose_name': 'Карточка', 'verbose_name_plural': 'Карточки'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ('-created_time',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='employeerate',
            options={'verbose_name': 'Зарплата', 'verbose_name_plural': 'Зарплаты'},
        ),
        migrations.AlterModelOptions(
            name='tableexcel',
            options={'verbose_name': 'Таблица Excel', 'verbose_name_plural': 'Таблицы Excel'},
        ),
        migrations.AlterModelOptions(
            name='tableproject',
            options={'verbose_name': 'Таблица', 'verbose_name_plural': 'Таблицы'},
        ),
        migrations.AlterModelOptions(
            name='worker',
            options={'verbose_name': 'Работа', 'verbose_name_plural': 'Работы'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='telegram_id',
            field=models.CharField(max_length=35, null=True, verbose_name='Telegram ID'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='comment',
            field=models.ManyToManyField(through='utv_api.CommentsCards', to='utv_api.comments', verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='deadline',
            field=models.DateTimeField(verbose_name='Дедлайн'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='description',
            field=models.TextField(verbose_name='Описание проекта'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='performers',
            field=models.ManyToManyField(blank=True, related_name='CardEvent', to=settings.AUTH_USER_MODEL, verbose_name='Исполнители'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='table',
            field=models.ManyToManyField(through='utv_api.TableCards', to='utv_api.tableproject', verbose_name='Таблицы'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название проекта'),
        ),
        migrations.AlterField(
            model_name='cards',
            name='worker',
            field=models.ManyToManyField(through='utv_api.WorkerCards', to='utv_api.worker', verbose_name='Рабочее время сотрудников'),
        ),
        migrations.AlterField(
            model_name='employeerate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employeerate', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
