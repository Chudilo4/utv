# Generated by Django 4.1.5 on 2023-01-23 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utv_smeta', '0004_time_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_time', models.TimeField(default=0, verbose_name='Фактическое время')),
                ('scheduled_time', models.TimeField(default=0, verbose_name='Плановое время')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utv_smeta.cards')),
            ],
        ),
        migrations.DeleteModel(
            name='Time',
        ),
    ]