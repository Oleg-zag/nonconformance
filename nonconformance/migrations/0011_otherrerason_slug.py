# Generated by Django 3.2.13 on 2023-02-28 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonconformance', '0010_alter_otherrerason_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherrerason',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
