# Generated by Django 3.2.13 on 2022-08-10 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_task_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='bom',
            field=models.ManyToManyField(blank=True, null=True, to='posts.Ebom0000'),
        ),
    ]
