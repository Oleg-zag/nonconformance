# Generated by Django 3.2.13 on 2022-08-16 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20220816_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ebom0000',
            name='critical',
        ),
        migrations.RemoveField(
            model_name='ebom0000',
            name='level',
        ),
        migrations.RemoveField(
            model_name='ebom0000',
            name='seriality',
        ),
        migrations.AlterField(
            model_name='ebom0000',
            name='state',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
