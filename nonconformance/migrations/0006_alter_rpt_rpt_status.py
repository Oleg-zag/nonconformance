# Generated by Django 3.2.13 on 2023-02-25 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonconformance', '0005_auto_20230225_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpt',
            name='rpt_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rpt', to='nonconformance.nnstatus'),
        ),
    ]
