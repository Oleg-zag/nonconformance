# Generated by Django 3.2.13 on 2022-11-07 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0029_auto_20221031_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, choices=[('VTX MANUFACTURING ENGINEERING', 'VTX MANUFACTURING ENGINEERING'), ('VTX SUPPLY CHAIN', 'VTX SUPPLY CHAIN'), ('VTX SHOP FLOOR', 'VTX SHOP FLOOR'), ('VTX PRODUCTION QUALITY', 'VTX PRODUCTION QUALITY'), ('VTX MATERIAL PLANING', 'VTX MATERIAL PLANING'), ('VTX MANAGMENT GROUP', 'VTX MANAGMENT GROUP'), ('OFFICE OF AIRWORTHINESS', 'OFFICE OF AIRWORTHINESS'), ('DESIGN OFFICE LEAD ENGINEERE ELECTRICAL PROVISIONS', 'EPS&EWIS'), ('DESIGN OFFICE LEAD ENGINEER FUEL SYSTEM', 'FUEL SYSTEM'), ('ADMIN', 'ADMIN')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, choices=[('MANUFACTURING ENGINEER', 'MANUFACTURING ENGINEER'), ('MANUFACTURING ENGINEER LEAD', 'MANUFACTURING ENGINEER LEAD'), ('MANUFACTURING ENGINEER MANAGER', 'MANUFACTURING ENGINEER MANAGER'), ('MANUFACTURING ENGINEER PLANER', 'MANUFACTURING ENGINEER PLANER'), ('PRODUCTION MANAGER', 'PRODUCTION MANAGER'), ('LEAD', 'LEAD ENGINEER'), ('HEAD', 'OFFICE HEAD'), ('ADMIN', 'ADMIN')], max_length=50, null=True),
        ),
    ]