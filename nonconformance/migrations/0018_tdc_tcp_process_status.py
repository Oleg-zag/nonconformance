# Generated by Django 3.2.14 on 2023-04-20 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonconformance', '0017_alter_nnstatus_nn_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='tdc',
            name='tcp_process_status',
            field=models.CharField(blank=True, choices=[('PREPARED', 'PREPARED'), ('APPROVED', 'APPROVED')], max_length=100, null=True),
        ),
    ]
