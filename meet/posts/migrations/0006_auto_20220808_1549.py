# Generated by Django 3.2.13 on 2022-08-08 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20220805_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('shot_name', models.CharField(max_length=3)),
                ('country', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('adress', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='group',
            name='user_list',
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, help_text='Group?', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post', to='posts.group', verbose_name='Group'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('department', models.CharField(blank=True, choices=[('VTX MANUFACTURING ENGINEERING', 'VTX MANUFACTURING ENGINEERING'), ('VTX SUPPLY CHAIN', 'VTX SUPPLY CHAIN'), ('VTX SHOP FLOOR', 'VTX SHOP FLOOR'), ('VTX PRODUCTION QUALITY', 'VTX PRODUCTION QUALITY'), ('VTX MATERIAL PLANING', 'VTX MATERIAL PLANING'), ('VTX MANAGMENT GROUP', 'VTX MANAGMENT GROUP')], max_length=50, null=True)),
                ('role', models.CharField(blank=True, choices=[('MANUFACTURING ENGINEER', 'MANUFACTURING ENGINEER'), ('MANUFACTURING ENGINEER LEAD', 'MANUFACTURING ENGINEER LEAD'), ('MANUFACTURING ENGINEER MANAGER', 'MANUFACTURING ENGINEER MANAGER'), ('MANUFACTURING ENGINEER PLANER', 'MANUFACTURING ENGINEER PLANER'), ('PRODUCTION MANAGER', 'PRODUCTION MANAGER')], max_length=50, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='posts.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]