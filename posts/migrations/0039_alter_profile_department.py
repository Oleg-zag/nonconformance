# Generated by Django 3.2.14 on 2023-04-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0038_auto_20230308_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, choices=[('VTX MANUFACTURING ENGINEERING', 'VTX MANUFACTURING ENGINEERING'), ('VTX SUPPLY CHAIN', 'VTX SUPPLY CHAIN'), ('VTX SHOP FLOOR', 'VTX SHOP FLOOR'), ('VTX PRODUCTION QUALITY', 'VTX PRODUCTION QUALITY'), ('VTX MATERIAL PLANING', 'VTX MATERIAL PLANING'), ('VTX MANAGMENT GROUP', 'VTX MANAGMENT GROUP'), ('OFFICE OF AIRWORTHINESS', 'OAW'), ('DESIGN OFFICE LEAD ENGINEERE ELECTRICAL PROVISIONS', 'EPS&EWIS'), ('DESIGN OFFICE ENGINEER FUEL SYSTEM', 'DOFS'), ('ADMIN', 'ADMIN'), ('CONFIGURATION MANAGMENT OFFICE', 'CM'), ('DESIGN OFFICE', 'DO'), ('DESIGN OFFICE ENGINEER STRUCTURE', 'DOSTR'), ('DESIGN OFFICE ENGINEER STRESS', 'DOSTRS'), ('DESIGN OFFICE ENGINEER POWER PLANT', 'DOPWD'), ('DESIGN OFFICE ENGINEER MATERIAL AND PROCESS', 'DOM&P'), ('PRODUCT ORGANIZATION', 'PRODUCT ORGANIZATION')], max_length=50, null=True),
        ),
    ]
