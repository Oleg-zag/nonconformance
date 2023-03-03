# Generated by Django 3.2.13 on 2022-08-17 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_tasks_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group',
            field=models.CharField(blank=True, choices=[('GENERAL', 'GNRL'), ('ME ELECTRICAL', 'MELC'), ('ME STRUCTURAL', 'MSTR'), ('ME EQUPMENT', 'MEQP'), ('ME FUNCTIONAL TEST', 'MFTS')], max_length=50, null=True),
        ),
    ]