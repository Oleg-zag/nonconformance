# Generated by Django 3.2.13 on 2022-10-31 13:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0029_auto_20221031_1359'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Nnstatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Nonconformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nn_name', models.CharField(max_length=20)),
                ('nn_type', models.CharField(choices=[('MDR', 'MDR'), ('PP', 'PP'), ('DCP', 'DCP')], max_length=3)),
                ('reason', models.CharField(choices=[('Airworthiness', 'Airworthiness'), ('Functional improvement', 'Functional improvement'), ('Customer request', 'Customer request'), ('Procurement difficulties', 'Procurement difficulties'), ('Cost reduction', 'Cost reduction'), ('Production process improvement', 'Production process improvement'), ('Other', 'Other')], max_length=100)),
                ('description_of_change', models.TextField()),
                ('solutions', models.TextField()),
                ('applicant_date', models.DateField(auto_now_add=True)),
                ('doa_decision', models.TextField(blank=True, null=True)),
                ('request_evaluation', models.CharField(blank=True, choices=[('REJECTED', 'REJECTED'), ('ACCEPTED', 'ACCEPTED')], max_length=100, null=True)),
                ('annex', models.FileField(blank=True, upload_to='posts/')),
                ('applicability', models.ManyToManyField(to='posts.Prototype')),
                ('applicant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='app', to='posts.profile')),
                ('cdo_signature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='c_d_o', to=settings.AUTH_USER_MODEL)),
                ('impact_areas_proposal', models.ManyToManyField(blank=True, null=True, related_name='i_a_p', to='posts.Profile')),
                ('nn_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='nn', to='nonconformance.nnstatus')),
                ('oaw', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='o_a_w', to='posts.profile')),
                ('part_number', models.ManyToManyField(blank=True, null=True, to='posts.Ebom0000')),
            ],
        ),
    ]