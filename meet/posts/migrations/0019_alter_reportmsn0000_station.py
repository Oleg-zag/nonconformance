# Generated by Django 3.2.13 on 2022-08-16 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_auto_20220816_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportmsn0000',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='posts.shopeflore'),
        ),
    ]
