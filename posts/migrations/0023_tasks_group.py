# Generated by Django 3.2.13 on 2022-08-17 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_auto_20220817_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='posts.group'),
        ),
    ]
