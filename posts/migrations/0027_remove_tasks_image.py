# Generated by Django 3.2.13 on 2022-10-21 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0026_tasks_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='image',
        ),
    ]
