# Generated by Django 3.2.14 on 2023-04-25 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nonconformance', '0021_alter_nnstatus_nn_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='dcp',
            name='constrained_dcp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_dcp', to='nonconformance.dcp'),
        ),
    ]
