# Generated by Django 4.1.5 on 2023-03-13 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utv_api', '0008_alter_event_created_time_alter_event_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tableproject',
            old_name='planed_actors_salary',
            new_name='planned_actors_salary',
        ),
    ]
