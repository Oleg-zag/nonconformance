# Generated by Django 3.2.13 on 2023-02-28 13:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0036_alter_profile_department'),
        ('nonconformance', '0007_rename_rpt_process_status_prtreviewstatus_rpt_review_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='NN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nn_name', models.CharField(max_length=20)),
                ('pp_status', models.BooleanField()),
                ('pp_date', models.DateField(auto_now_add=True)),
                ('vertex_doc', models.CharField(max_length=100)),
                ('purchase_order', models.CharField(max_length=100)),
                ('drawing_issue', models.CharField(max_length=100)),
                ('batch_qty', models.IntegerField()),
                ('defective_qty', models.IntegerField()),
                ('manufacture_po', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('defect_descriptions', models.TextField()),
                ('defect_descriptions_image', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Picture')),
                ('mdr_pn', models.CharField(max_length=100)),
                ('mdr_lot', models.CharField(max_length=100)),
                ('defect_cause', models.TextField()),
                ('defect_cause_image', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Picture')),
                ('ca_to_remove_case', models.BooleanField(blank=True, null=True)),
                ('complete_before', models.CharField(max_length=100)),
                ('solutions', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('doa_decision', models.TextField(blank=True, null=True)),
                ('request_evaluation', models.CharField(blank=True, choices=[('REJECTED', 'REJECTED'), ('ACCEPTED', 'ACCEPTED')], max_length=100, null=True)),
                ('annex', models.FileField(blank=True, upload_to='posts/')),
                ('initiater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='initiater', to='posts.profile')),
                ('inspector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='insp', to='posts.profile')),
                ('inspector_date', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='inspdate', to='posts.profile')),
                ('model', models.ManyToManyField(to='posts.Prototype')),
                ('nn_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nonconformance.nnstatus')),
                ('oaw', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ow', to='posts.profile')),
                ('part_number', models.ManyToManyField(blank=True, null=True, to='posts.Ebom0000')),
                ('pp_initiater_signature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ppsignature', to='posts.profile')),
            ],
        ),
        migrations.AlterField(
            model_name='prtprocessstatus',
            name='rpt_process_status',
            field=models.CharField(choices=[('DISPATCHED', 'DISPATCHED'), ('SENT FOR DE REVIEW', 'SENT FOR DE REVIEW'), ('RPT RECEIVED BY DE/CVE', 'RPT RECEIVED BY DE/CVE'), ('SENT FOR OAW REVIEW', 'SENT FOR OAW REVIEW'), ('CLOSURE', 'CLOSURE')], max_length=40),
        ),
        migrations.CreateModel(
            name='OtherRerason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='oth', to=settings.AUTH_USER_MODEL)),
                ('dcp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='oth', to='nonconformance.dcp')),
                ('nn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='oth', to='nonconformance.nn')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='nn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='com', to='nonconformance.nn'),
        ),
        migrations.AddField(
            model_name='rpt',
            name='nn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='nn', to='nonconformance.nn'),
        ),
    ]
